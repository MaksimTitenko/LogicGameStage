from django.views.generic.base import TemplateView
from django.contrib.auth import login, authenticate

from RoundTable.models import UserAccount
from .forms import LoginForm, RegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import auth
from www_game_site import settings

import facebook
import json
from httplib2 import Http
import vk


class HomePageView(TemplateView):
    template_name = 'RoundTable/base/index.html'


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
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']

        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
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
    context = {'form': form}
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


class UserAccountView(generic.View):
    template_name = 'user_account.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        context = {
            'current_user': user,
        }
        return render(self.request, self.template_name, context)
