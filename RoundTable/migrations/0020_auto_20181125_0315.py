# Generated by Django 2.1.2 on 2018-11-25 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoundTable', '0019_invite_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]