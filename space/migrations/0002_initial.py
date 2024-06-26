# Generated by Django 4.2.7 on 2024-01-02 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('useraccount', '0001_initial'),
        ('space', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='spacepost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='spacefile',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_files', to='space.spacepost'),
        ),
        migrations.AddField(
            model_name='space',
            name='category',
            field=models.ManyToManyField(related_name='spaces', to='useraccount.category'),
        ),
        migrations.AddField(
            model_name='space',
            name='exclude_users',
            field=models.ManyToManyField(blank=True, related_name='spaces_excluded', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='space',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='spaces_followed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='space',
            name='include_users',
            field=models.ManyToManyField(blank=True, related_name='spaces_included', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='space.spacepost'),
        ),
    ]
