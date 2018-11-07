from __future__ import unicode_literals
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django_extensions import settings
from django.utils.text import slugify


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

    def avatar_upload_to(self, filename):
        return os.path.join('RoundTable/avatars/', self.username + os.path.splitext(filename)[1])

    username = models.CharField(max_length=30, verbose_name='Логин', unique=True)
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Эл.почта', unique=True)

    middle_name = models.CharField(max_length=30, verbose_name='Отчество')
    gender = models.CharField(max_length=7, verbose_name='Пол', choices=SEX_CHOICES)
    date_birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone = models.CharField(max_length=15, verbose_name='Контактный телефон', blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, null=True, blank=True,
                               default='RoundTable/default_avatar/default.png', verbose_name='Аватар')
    bio = models.TextField(max_length=400, blank=True, verbose_name='О себе')
    singleplayer = models.IntegerField(default=0, verbose_name='Одиночных игр: ')
    multiplayer = models.IntegerField(default=0, verbose_name='Командных игр: ')
    singleplayer_answers = models.IntegerField(default=0, verbose_name='Ответов в одиночной игре: ')
    total_count_of_questions = models.IntegerField(default=0, verbose_name='Количество отыгранных вопросов: ')

    def __str__(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name)
    # Если захочется сделать UserAccount для каждого пользователя с возможностью просмотра понадобится этот код

    # def get_absolute_url(self):
    #     return reverse('account_view', kwargs={'user': self.username})

    # плейсхолдеры для телефона, мыла и даты рождения!


class TeamMod(models.Model):
    team_name = models.CharField(max_length=30, verbose_name='Название пространсва')
    slug = models.SlugField(max_length=30)
    number_of_all_games = models.PositiveIntegerField(default=0)
    number_of_correct_answers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Команда {self.team_name}'

    def get_absolute_url(self):
        return reverse('team_mod', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        """
        Takes a model instance, sluggable field name (such as 'title') of that
        model as string, slug field name (such as 'slug') of the model as string;
        returns a unique slug as string.
        """
        slug = slugify(self.team_name)
        unique_slug = slug
        extension = 1
        while TeamMod.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, extension)
            extension += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        super().save(*args, **kwargs)


class UserInTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(TeamMod, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)

    def __str__(self):
        return f'Пользователь {self.user.username} в команде {self.team.team_name}'


class Invite(models.Model):
    slug = models.SlugField()
    user_for = models.OneToOneField(User, on_delete=models.CASCADE)
    username_from = models.CharField(max_length=30)
    team = models.ForeignKey(TeamMod, on_delete=models.CASCADE)

    def __str__(self):
        return f'Инвайт от {self.username_from.username} в команду {self.team.team_name} для {self.user_for}'
