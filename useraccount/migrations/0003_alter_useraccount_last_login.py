# Generated by Django 4.2.7 on 2023-11-07 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0002_alter_useraccount_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
