# Generated by Django 4.2.7 on 2023-12-16 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0003_remove_verificationprorequest_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='id_card',
            field=models.FileField(blank=True, null=True, upload_to='id_card'),
        ),
    ]