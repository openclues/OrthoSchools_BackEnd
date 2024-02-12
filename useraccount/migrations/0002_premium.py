# Generated by Django 4.2.7 on 2024-01-06 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Premium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('professional_title', models.CharField(max_length=255)),
                ('license_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('email_address', models.EmailField(max_length=254)),
                ('clinic_name', models.CharField(max_length=255)),
                ('clinic_address', models.TextField()),
                ('education', models.TextField()),
                ('graduation_year', models.IntegerField()),
                ('certifications', models.TextField()),
                ('experience', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='premium', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
