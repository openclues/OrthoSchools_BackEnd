# Generated by Django 4.2.7 on 2023-11-16 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0008_alter_useraccount_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='cover'),
        ),
    ]
