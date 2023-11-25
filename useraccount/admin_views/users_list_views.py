from django.contrib import admin
from useraccount.models import UserAccount


class UserAccountAdmin(admin.ModelAdmin):
    change_list_template = '/admin/users_list.html'

    def changelist_view(self, request, extra_context=None):
        # Add additional context data to pass to the template
        extra_context = extra_context or {}
        extra_context['total_count'] = UserAccount.objects.count()
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(UserAccount, UserAccountAdmin)
