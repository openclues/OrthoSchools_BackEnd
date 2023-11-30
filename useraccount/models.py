from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# managers.py
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None,  **extra_fields):
        if not email and not username:
            raise ValueError('At least one of email or username is required.')
        username = email.split('@')[0] + email.split('@')[1]
        email = self.normalize_email(email)
        # generate username from email

        # username = email
        #print first_name
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        # if email and not username:
        #     extra_fields['username'] = None
        #
        # elif username and not email:
        #     extra_fields['email'] = None

        user = self.model(username=username, email=email, **extra_fields)
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
        (2, 'Premium Dentist'),
    )
    is_verified = models.BooleanField(default=False)
    is_verified_pro = models.BooleanField(default=False)
    is_suspend = models.BooleanField(default=False)
    userRole = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, default=1)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    is_banned = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    objects = UserManager()


class Certificate(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    certificateFile = models.FileField(upload_to='certificateFile', blank=True, null=True)
    profile = models.ForeignKey("useraccount.ProfileModel", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.profile.user.email


class ProfileModel(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    study_in = models.CharField(max_length=100, blank=True, null=True)
    cover = models.ImageField(upload_to='cover', blank=True, null=True)
    profileImage = models.ImageField(upload_to='profileImage', blank=True)
    place_of_work = models.CharField(max_length=100, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)
    selfie = models.ImageField(upload_to='selfie', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.user.username


@receiver(post_save, sender=UserAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)

#
# @receiver(post_save, sender=UserAccount)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profilemodel.save()
