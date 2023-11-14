from django.db import models

from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField


class Space(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Define choices for user types with more readable keys
    USER_TYPES = (
        ('basic student', 'Basic Student'),
        ('premium student', 'Premium Student'),
        ('blogger', 'Blogger'),
    )

    # Field to specify allowed user types in the space
    allowed_user_types = MultiSelectField(choices=USER_TYPES, max_choices=3, max_length=100, default='basic student')

    # Field to specify excluded users

    # Field to specify included users
    exclude_users = models.ManyToManyField("useraccount.UserAccount", related_name='spaces_excluded', blank=True)
    include_users = models.ManyToManyField("useraccount.UserAccount", related_name='spaces_included', blank=True)

    # Field to specify if joining is optional
    is_optional_for_basic_students = models.BooleanField(default=True)
    is_optional_for_premium_students = models.BooleanField(default=True)
    is_optional_for_bloggers = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SpaceFile(models.Model):
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
