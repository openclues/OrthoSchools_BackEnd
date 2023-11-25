from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# managers.py
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractUser):
    USER_ROLE_CHOICES = (
        (1, 'Basic Dentist'),
        (2, 'Blogger')
    )

    userRole = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, default=1)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    is_banned = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    objects = UserManager()


class Certificate(models.Model):
    number = models.CharField(max_length=100, blank=True, null=True)
    certificateFile = models.FileField(upload_to='certificateFile', blank=True, null=True)
    profile = models.ForeignKey("useraccount.ProfileModel", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.profile.user.email


class ProfileModel(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    cover = models.ImageField(upload_to='cover', blank=True, null=True)
    profileImage = models.ImageField(upload_to='profileImage', blank=True)
    place_of_work = models.CharField(max_length=100, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_verified_pro = models.BooleanField(default=False)
    selfie = models.ImageField(upload_to='selfie', blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


@receiver(post_save, sender=UserAccount)
def save_user_profile(sender, instance, **kwargs):
    instance.profilemodel.save()




