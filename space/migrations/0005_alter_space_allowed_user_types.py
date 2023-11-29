# Generated by Django 4.2.7 on 2023-11-26 19:47

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0004_alter_space_allowed_user_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='allowed_user_types',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Basic Dentist'), (2, 'Premium Dentist')], default='basic student', max_length=100),
        ),
    ]
