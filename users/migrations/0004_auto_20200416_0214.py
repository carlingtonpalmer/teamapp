# Generated by Django 2.2.9 on 2020-04-16 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200413_0147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='user',
            name='regulation_number',
        ),
    ]
