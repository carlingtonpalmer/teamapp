# Generated by Django 2.2.9 on 2020-04-15 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_type', models.CharField(max_length=50)),
                ('chassis', models.CharField(max_length=100)),
                ('cost', models.CharField(max_length=10)),
                ('vehicle_use', models.CharField(max_length=50)),
                ('claim_free_driving', models.CharField(max_length=200)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
