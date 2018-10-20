from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from .views import (
    HomePageView,
    registration_view,
    login_view,
    CallbackView,
    UserAccountView)

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('user_account/<str:user>', UserAccountView.as_view(), name='account_view'),
    path('registration/', registration_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),

    path('vk_login/', RedirectView.as_view(url=settings.VK_REDIRECT), name='vk_login'),
    path('vk_callback/', CallbackView.vk_callback, name='vk_callback'),
    path('facebook_login/', RedirectView.as_view(url=settings.FACEBOOK_REDIRECT), name='facebook_login'),
    path('facebook_callback/', CallbackView.facebook_callback, name='facebook_callback'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
