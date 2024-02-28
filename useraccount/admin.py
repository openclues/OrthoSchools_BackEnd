from actstream.models import Action
from django.contrib import admin
from django.shortcuts import render
from django.contrib import admin
from django.http import HttpRequest
from django.utils import timezone
from django.utils.html import format_html
from unfold.decorators import action
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from space.models import Space
from .models import UserAccount, ProfileModel, Certificate, Category, VerificationProRequest, PremiumRequest, Premium
from django.contrib.auth.admin import UserAdmin


class CustomAdminIndexView(admin.AdminSite):
    def index(self, request, extra_context=None):
        spaces = Space.objects.all()  # Replace with your actual model and queryset logic

        context = {
            'title': 'Dashboard',
            'subtitle': 'Custom Dashboard View',
            'spaces': spaces,
        }

        if extra_context is not None:
            context.update(extra_context)

        return render(request, 'admin/index.html', context)


# Register the custom admin site
custom_admin_site = CustomAdminIndexView(name='custom_admin')


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
    search_fields = ('', 'bio', 'place_of_work', 'speciality', 'selfie')


admin.site.register(ProfileModel, ProfileAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'userRole', 'is_staff', 'is_active',)


admin.site.register(UserAccount, CustomUserAdmin)

admin.site.unregister(UserAccount)


@admin.register(UserAccount)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    actions_submit_line = ["submit_line_action_activate"]

    list_display = (
        'first_name', 'last_name', 'userRole', 'email', 'created_since', 'is_verified', 'is_verified_pro', 'is_suspend', 'email_verified', 'phone_verified',)
    list_filter = UserAdmin.list_filter + ('userRole',)
    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('userRole',)}),
        ('Verification', {'fields': ('is_verified', 'is_verified_pro', 'is_suspend','email_verified','phone_verified')}
         ))

    def created_since(self, obj):
        return str((timezone.now() - obj.date_joined).days) + " days ago"

    @action(description="Suspend User")
    def submit_line_action_activate(self, request, queryset):
        for user in queryset:
            if user.is_suspend:
                # If user is already suspended, show "Unsuspend" action
                self.message_user(request, "User is already suspended.")
            else:
                # If user is not suspended, suspend the user
                user.is_suspend = True
                user.save()
                self.message_user(request, "User Suspended Successfully.")


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')


class UserInline(admin.StackedInline):
    model = UserAccount
    can_delete = False
    verbose_name_plural = 'User'


@admin.register(VerificationProRequest)
class VerificationProRequestAdmin(ModelAdmin):
    pass

@admin.register(Premium)
class PremiumAdmin(ModelAdmin):
    pass
@admin.register(PremiumRequest)
class PremiumRequestAdmin(ModelAdmin):
    pass
    # add action button
    # actions_submit_line = ["submit_line_action_activate"]
    # list_display = ('user_first_name',)

    # def queryset(self, request):
    #     qs = super(PremiumRequestAdmin, self).queryset(request)
    #     self.request = request
    #     return qs
    #
    # @action(description="Accept Request")
    # def submit_line_action_activate(self, request, queryset):
    #     requests = self.get_object(
    #         request, queryset
    #
    #     )
    #     requests.requestStatus = 'accepted'

    # def get_user_first_name(self, obj):
    #     return obj.profile.user.first_name
