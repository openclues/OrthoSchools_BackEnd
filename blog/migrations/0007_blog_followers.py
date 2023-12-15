# Generated by Django 4.2.7 on 2023-12-13 19:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_blog_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='blog_followed', to=settings.AUTH_USER_MODEL),
        ),
    ]
