
#shoe profile screen
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.base import Token
from django.views import View

from useraccount.models import ProfileModel


class ShowProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = ProfileModel.objects.get(user=user)
        return render(request, 'profile/settings.html', {'profile': profile, 'user': user, 'request': request})

