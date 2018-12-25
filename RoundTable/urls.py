from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from .views import (
    registration_view,
    login_view,
    CallbackView,
    UserAccountView,
    CreateTeamView,
    TeamView,
    SearchView,
    AddInviteView,
    ConfirmInviteView,
    DeleteUserFromTeamView,
    AccountPartial,
    NotificationsPartial, QuestionView)

urlpatterns = [
    path('', CreateTeamView.as_view(), name='index'),
    path('team_mod/<slug:slug>', TeamView.as_view(), name='team_mod'),


    path('profile/', UserAccountView.as_view(), name='account_view'),
    path('profile/account', AccountPartial.as_view(), name='account'),
    path('profile/notifications', NotificationsPartial.as_view(), name='notifications'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('confirm_invite', ConfirmInviteView.as_view(), name='confirm_invite'),
    path('delete_user/', DeleteUserFromTeamView.as_view(), name='delete_user'),
    path('search/', SearchView.as_view(), name='search'),
    path('add_invite', AddInviteView.as_view(), name='add_invite'),
    path('vk_login/', RedirectView.as_view(url=settings.VK_REDIRECT), name='vk_login'),
    path('vk_callback/', CallbackView.vk_callback, name='vk_callback'),
    path('facebook_login/', RedirectView.as_view(url=settings.FACEBOOK_REDIRECT), name='facebook_login'),
    path('facebook_callback/', CallbackView.facebook_callback, name='facebook_callback'),
    path('game/<slug:slug>', QuestionView.as_view(), name='game_mod')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
