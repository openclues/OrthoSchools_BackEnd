from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.views import View
from .models import Blog


class BlogDetailView(View):
    template_name = 'blog_detail.html'  # Adjust the template name as needed

    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        return render(request, self.template_name, {'blog': blog})


class AdminHomeScreenView(View):
    template_name = 'admin/index.html'  # Adjust the template name as needed

    def get(self, request):
        return render(request, self.template_name, {})
