# Generated by Django 3.1.7 on 2021-06-07 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ubek', '0014_auto_20210606_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]