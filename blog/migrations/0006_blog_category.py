# Generated by Django 4.2.7 on 2023-12-13 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
        ('blog', '0005_alter_blogpost_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ManyToManyField(related_name='blogs', to='useraccount.category'),
        ),
    ]
