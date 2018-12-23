from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import dateformat
from django.utils.text import slugify

from www_game_site import settings


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
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name)


class TeamMod(models.Model):
    team_name = models.CharField(max_length=30, verbose_name='Название пространсва')
    slug = models.SlugField(max_length=30)
    number_of_all_games = models.PositiveIntegerField(default=0)
    number_of_correct_answers = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.team_name}'

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
    user_for = models.ForeignKey(User, null=True, unique=False, related_name='user_for', on_delete=models.CASCADE)
    user_from = models.ForeignKey(User, null=True, unique=False, related_name='user_from', on_delete=models.CASCADE)
    team = models.ForeignKey(TeamMod, on_delete=models.CASCADE)
    date_sand = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Инвайт от {self.user_from.username} в команду {self.team.team_name} для {self.user_for.username}'

    def date_converter(self):
        months = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
                  9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}
        return f'{self.date_sand.day} {months[self.date_sand.month]} {self.date_sand.year}'


class Answers(models.Model):
    answer = models.CharField(max_length=100)


class ListOffset(models.Model):
    offset = models.CharField(max_length=100, verbose_name='Зачёт')


class QuestionTopic(models.Model):
    topic = models.CharField(max_length=100, verbose_name='Тема')


class Question(models.Model):
    def image_upload_to(self, filename):
        return os.path.join('RoundTable/images/', self.text + os.path.splitext(filename)[1])

    text = models.CharField(max_length=300, verbose_name='Текст вопроса')
    comment = models.CharField(max_length=255, verbose_name='Комментарий')
    image = models.ImageField(upload_to=image_upload_to, null=True, blank=True, verbose_name='Пикча')
    answers = models.ForeignKey(Answers, on_delete=models.CASCADE)
    topics = models.ForeignKey(QuestionTopic, on_delete=models.SET_NULL)
    offsets = models.ForeignKey(ListOffset, on_delete=models.SET_NULL)


