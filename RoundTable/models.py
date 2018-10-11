from __future__ import unicode_literals
import os
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    SEX_CHOICES = (
        ('Мужчина', u"Мужчина"),
        ('Женщина', u"Женщина"),
    )

    COUNTRIES = (
        ('Беларусь', 'Беларусь'),
        ('Россия', 'Россия'),
        ('Украина', 'Украина')
    )

    class Meta:
        db_table = 'auth_user'

    def avatar_upload_to(instance, filename):
        return os.path.join('RoundTable/avatars/', instance.username + os.path.splitext(filename)[1])

    username = models.CharField(max_length=30, verbose_name='Логин', unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Эл.почта', unique=True)

    middle_name = models.CharField(max_length=30, verbose_name='Отчество')
    gender = models.CharField(max_length=7, verbose_name='Пол', choices=SEX_CHOICES)
    date_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone = models.CharField(max_length=15, verbose_name='Контактный телефон', blank=True)
    country = models.CharField(max_length=40, choices=COUNTRIES, default=COUNTRIES[0][0], verbose_name='Страна')
    city = models.CharField(max_length=40, blank=True, verbose_name='Город')
    avatar = models.ImageField(upload_to=avatar_upload_to, null=True, blank=True, verbose_name='Аватар')
    bio = models.TextField(max_length=400, blank=True, verbose_name='О себе')
    singleplayer = models.IntegerField(default=0, verbose_name='Одиночных игр: ')
    multiplayer = models.IntegerField(default=0, verbose_name='Командных игр: ')
    singleplayer_answers = models.IntegerField(default=0, verbose_name='Ответов в одиночной игре: ')
    total_count_of_questions = models.IntegerField(default=0, verbose_name='Количество отыгранных вопросов: ')

    def __str__(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name)

    # плейсхолдеры для телефона, мыла и даты рождения!
