from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import Blog, BlogPost
from rest_framework import generics

from .serializers import BlogSerializer


class PaginationList(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class BlogDetailView(View):
    template_name = 'blog_detail.html'  # Adjust the template name as needed

    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        return render(request, self.template_name, {'blog': blog})


class AdminHomeScreenView(View):
    template_name = 'admin/index.html'  # Adjust the template name as needed

    def get(self, request):
        return render(request, self.template_name, {})


class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [SearchFilter]
    pagination_class = PaginationList
    search_fields = ['category__name']  # Assuming 'name' is a field in your Category model

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_latest_created_posts(self):
        blogs = BlogPost.objects.filter(blog__is_published=True).order_by('-updated_at')[:5]
        return BlogSerializer(blogs, many=True).data

