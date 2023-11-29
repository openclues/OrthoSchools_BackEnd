# Generated by Django 4.2.7 on 2023-11-27 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(blank=True, max_length=100, null=True)),
                ('course_description', models.TextField()),
                ('course_image', models.ImageField(blank=True, null=True, upload_to='course_images')),
                ('course_video', models.FileField(blank=True, null=True, upload_to='course_videos')),
                ('course_link', models.URLField()),
            ],
        ),
    ]