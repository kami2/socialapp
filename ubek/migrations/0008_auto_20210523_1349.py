# Generated by Django 3.1.7 on 2021-05-23 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ubek', '0007_auto_20210523_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postwall',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
