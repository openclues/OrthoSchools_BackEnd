from django.contrib.auth.models import AbstractUser
from django.db import models


class UserAccount(AbstractUser):
    # user type choices from premium to basic
    USER_TYPE_CHOICES = (
        (1, 'Premium'),
        (2, 'Basic'),
    )

# choises of user role between student, dentist and bloggers
    USER_ROLE_CHOICES = (
        (1, 'Student'),
        (2, 'Dentist'),
        (3, 'Blogger'),
        (4, 'User'),
    )
    userRole = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, default=1)
    userType = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class ProfileModel(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profileImage = models.ImageField(upload_to='profileImage', blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
