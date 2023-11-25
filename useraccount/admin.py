from django.contrib import admin

from space.models import Space
from .models import UserAccount, ProfileModel, Certificate
from django.contrib.auth.admin import UserAdmin


class CertificateInline(admin.StackedInline):
    model = Certificate
    extra = 0

    can_delete = False
    verbose_name_plural = 'Certificate'


class ProfileAdmin(admin.ModelAdmin):
    inlines = (CertificateInline,)
    list_display = (
        'user',
        'email',
        'phone',
        'bio',
        'place_of_work',
        'speciality',
        'is_verified',
        'is_verified_pro',
        'selfie',
    )

    def user(self, obj):
        return obj.user.email

    def email(self, obj):
        return obj.user.email

    def phone(self, obj):
        # Assuming you have a 'phone' field in your User model
        return obj.user.phone if hasattr(obj.user, 'phone') else None

    user.short_description = 'Username'
    email.short_description = 'Email'
    phone.short_description = 'Phone'
# search
    search_fields = ('', 'bio', 'place_of_work', 'speciality', 'is_verified', 'is_verified_pro', 'selfie')

admin.site.register(ProfileModel, ProfileAdmin)


class CustomUserAdmin(UserAdmin):
    ...


admin.site.register(UserAccount, CustomUserAdmin)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from unfold.admin import ModelAdmin


admin.site.unregister(UserAccount)


@admin.register(UserAccount)
class UserAdmin(BaseUserAdmin, ModelAdmin):

    pass
