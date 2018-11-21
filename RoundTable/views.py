from django.db.models import Q
from django.template import RequestContext
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate

from RoundTable.models import User, TeamMod, UserInTeam, Invite
from .forms import LoginForm, RegistrationForm, CreateTeamForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy
from django.views import generic

from django.contrib import auth
from www_game_site import settings

import facebook
import json
from httplib2 import Http
import vk


# Вьюшки для авторизации и регистрации сделаны с использованием стандартной модели Юзера.
# Он импортирован выше.
# Это не окончательный вариант, потому что необходимо расширять ее добавлением другой информации, например, авы.
# В моделях я закомментировал свою наработку по этому поводу, можно глянуть, но не исправлять.
# Регистрация и авторизация работают, можете проверить, что пользователи создаются
# Проверяется через админку, которую запаролил Максим так, что я не могу в нее войти, ну и ладно.
# Возможно, надо создавать нового суперюзера
# Как я узнал, что они создаются? Очень просто: при регистрации вводил те же данные, выскакивало исключение.
# Если вы успешны, то вас редиректнет на главную страницу.

def registration_view(request):
    form = RegistrationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        avatar = form.cleaned_data['avatar']

        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.avatar = avatar
        new_user.save()

        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('index'))
    context = {'form': form,
               'current_view': 'registration_view'}
    return render(request, 'RoundTable/registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))

    context = {
        'form': form,
        'current_view': 'login'
    }

    return render(request, 'RoundTable/login.html', context)


####################################################################################################
# Класс посвящен авторизации через соцсети.
# Это одна из проблем, которые придется еще решить
# + кроме существующих функций нужно будет добавить еще авторизацию через google


class CallbackView(generic.View):

    @staticmethod
    def vk_callback(request):
        resp, content = Http().request(
            uri=settings.VK_URL + request.GET.get('code', ''),
            method='GET')

        content = json.loads(content.decode('ascii'))
        token = content['access_token']
        user_id = content['user_id']
        email = content['email']
        session = vk.Session(access_token=token)
        new_user_data = vk.API(session=session).users.get(user_ids=user_id)[0]
        username = "{0} {1}".format(new_user_data['first_name'], new_user_data['last_name'])

        if User.objects.filter(username=username).exists():
            new_user = User.objects.get(username=username)
        else:
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=user_id
            )

        auth.login(request, new_user)
        return HttpResponseRedirect(reverse_lazy('index'))

    @staticmethod
    def facebook_callback(request):

        code = request.GET.get('code', False)
        resp, content = Http().request(
            uri=settings.FACEBOOK_URL.format(client_id=settings.FACEBOOK_APP,
                                             client_secret=settings.FACEBOOK_SECRET,
                                             code=code, domain=settings.DOMAIN),
            method='GET')

        content = json.loads(content.decode('ascii'))
        token = content['access_token']
        session = facebook.GraphAPI(access_token=token)
        args = {'fields': 'name,email'}
        new_user_data = session.get_object(id='me', **args)
        username = new_user_data['name']
        if User.objects.filter(username=username).exists():
            new_user = User.objects.get(username=username)
        else:
            new_user = User.objects.create_user(
                username=username,
                email=new_user_data['email'],
                password=new_user_data['id']
            )
        auth.login(request, new_user)
        return HttpResponseRedirect(reverse_lazy('index'))


######################################################################################################

class UserAccountView(generic.View):
    template_name = 'RoundTable/user_account.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_in_team = UserInTeam.objects.filter(user=self.request.user)
        invites = Invite.objects.filter(user_for=self.request.user)
        context = {
            'user': user,
            'current_view': self.__class__.__name__
        }
        if user_in_team.exists():
            context['user_in_teams'] = user_in_team
        if invites.exists():
            context['invites'] = invites
        return render(self.request, self.template_name, context)


class TeamView(generic.View):
    template_name = 'RoundTable/team_mod.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        user = self.request.user
        current_team = TeamMod.objects.get(slug=slug)
        current_users = UserInTeam.objects.filter(user=user, team=current_team)
        user_captain = current_users.get(is_captain=True)
        context = {'current_view': self.__class__.__name__,
                   'user_captain': user_captain.user}

        if user.is_authenticated and current_users.exists():
            context['team'] = current_team
            context['users'] = current_users

            return render(self.request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))


class CreateTeamView(generic.View):
    template_name = 'RoundTable/base/index.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            form = CreateTeamForm()
            teams = UserInTeam.objects.filter(user=self.request.user)
            context = {
                'teams': teams,
                'form': form,
                'current_view': 'playModePage'
            }
            return render(self.request, self.template_name, context)
        else:
            return HttpResponseRedirect(reverse_lazy('login'))

    def post(self, request, *args, **kwargs):
        form = CreateTeamForm(request.POST or None)
        teams = UserInTeam.objects.filter(user=self.request.user)
        if teams.count() >= 5:
            form.add_error(None, 'Вы не можете создать более 5 команд')
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            current_team = TeamMod.objects.create(team_name=team_name)
            current_team.save()
            UserInTeam.objects.create(team=current_team, user=request.user, is_captain=True)
            return HttpResponseRedirect(
                reverse_lazy('team_mod', kwargs={'slug': current_team.slug}))

        context = {
            'teams': UserInTeam.objects.filter(user=self.request.user),
            'form': form
        }

        return render(self.request, self.template_name, context)


class SearchView(FormView):
    template_name = 'RoundTable/result.html'

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            q = self.request.GET.get('q')
            if q is not "":
                results = User.objects.filter(Q(username__startswith=q) | Q(last_name__istartswith=q))

                return render(self.request, self.template_name, {"results": results})
            else:
                return render(self.request, self.template_name, {})


class AddInviteView(generic.View):
    template_name = 'RoundTable/user_account.html'

    def post(self, request, *args, **kwargs):
        team_name = self.request.POST.get('team_name')
        username = self.request.POST.get('username')
        Invite.objects.create(slug=f'{username}{team_name}', team=TeamMod.objects.get(team_name=team_name),
                              username_from=request.user.username, user_for=User.objects.get(username=username))
        return JsonResponse({'ok': 'ok'})


class ConfirmInviteView(generic.View):
    template_name = 'RoundTable/user_account.html'

    def get(self, request, *args, **kwargs):
        invite_slug = self.request.GET.get('invite_slug')
        event = self.request.GET.get('event')
        invite = Invite.objects.get(slug=invite_slug)
        if event == '1':
            UserInTeam.objects.create(user=invite.user_for, team=invite.team)
        invite.delete()
        return JsonResponse({'ok': 'ok'})


class DeleteUserFromTeamView(generic.View):
    template_name = 'RoundTable/team_mod.html'

    def get(self, request, *args, **kwargs):
        username = self.request.GET.get('username')
        team_name = self.request.GET.get('team_name')
        user_in_team = UserInTeam.objects.get(team=TeamMod.objects.get(team_name=team_name),
                                              user=User.objects.get(username=username))
        user_in_team.delete()
        return JsonResponse({'ok':'ok'})
