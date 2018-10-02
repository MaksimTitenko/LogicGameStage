from __future__ import unicode_literals
#
# from django.db import models
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.utils.translation import ugettext_lazy as _
# from django.core.mail import send_mail
# from
# COUNTRIES = (
#     ('Беларусь','Беларусь'),
#     ('Россия','Россия'),
#     ('Украина','Украина')
# )
#
# class Profile(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(_('email address'), unique=True)
#     phone = models.CharField(_('phone'), unique=True)
#     first_name = models.CharField(_('first name'), max_length=30)
#     last_name = models.CharField(_('last name'), max_length=30)
#     date_birth = models.DateField(_('date_birth'),auto_now_add=True)
#     country = models.CharField(_('country'), choices=COUNTRIES, default=COUNTRIES[0][0])
#     city = models.CharField(_('city'), max_length=40, blank=True)
#     avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
#     bio = models.TextField(max_length=400, blank=True)
#     moder = models.
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#
#     def get_full_name(self):
#
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
#
#     def get_short_name(self):
#
#         return self.first_name
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#
#         send_mail(subject, message, from_email, [self.email], **kwargs)
