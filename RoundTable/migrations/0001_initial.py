# Generated by Django 2.1.1 on 2018-10-11 21:28

import RoundTable.models
import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Логин')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Эл.почта')),
                ('middle_name', models.CharField(max_length=30, verbose_name='Отчество')),
                ('gender', models.CharField(choices=[('Мужчина', 'Мужчина'), ('Женщина', 'Женщина')], max_length=7, verbose_name='Пол')),
                ('date_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='Контактный телефон')),
                ('country', models.CharField(choices=[('Беларусь', 'Беларусь'), ('Россия', 'Россия'), ('Украина', 'Украина')], default='Беларусь', max_length=40, verbose_name='Страна')),
                ('city', models.CharField(blank=True, max_length=40, verbose_name='Город')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=RoundTable.models.User.avatar_upload_to, verbose_name='Аватар')),
                ('bio', models.TextField(blank=True, max_length=400, verbose_name='О себе')),
                ('singleplayer', models.IntegerField(default=0, verbose_name='Одиночных игр: ')),
                ('multiplayer', models.IntegerField(default=0, verbose_name='Командных игр: ')),
                ('singleplayer_answers', models.IntegerField(default=0, verbose_name='Ответов в одиночной игре: ')),
                ('total_count_of_questions', models.IntegerField(default=0, verbose_name='Количество отыгранных вопросов: ')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
