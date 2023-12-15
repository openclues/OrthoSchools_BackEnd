# Generated by Django 4.2.7 on 2023-12-05 22:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('space', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='spaces_followed', to=settings.AUTH_USER_MODEL),
        ),
    ]
