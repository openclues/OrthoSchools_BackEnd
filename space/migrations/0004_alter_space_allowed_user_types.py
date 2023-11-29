# Generated by Django 4.2.7 on 2023-11-25 10:46

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_rename_is_optional_for_basic_space_is_optional_for_basic_students_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='allowed_user_types',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Basic Dentist'), (2, 'Blogger')], default='basic student', max_length=100),
        ),
    ]