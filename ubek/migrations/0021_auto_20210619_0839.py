# Generated by Django 3.1.7 on 2021-06-19 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubek', '0020_auto_20210614_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.TextField(default='Say something about yourself'),
        ),
    ]