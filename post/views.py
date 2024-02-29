from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer
from post.serializers import AddPostSerializer, SpacePostSerializer
from space.models import SpacePost, Space
from space.serializers import SpaceSerializer
from useraccount.serializers import RecommendedSpacesSerializer


class CreatePostApiView(generics.CreateAPIView):
    serializer_class = AddPostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        post_images = self.request.FILES.getlist('post_images')
        video = self.request.FILES.get('video')

        if video:
            serializer.instance.video = video
            serializer.instance.save()

        for image in post_images:
            print(image)
            serializer.instance.post_images.create(image=image)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid() is False:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(AddPostSerializer(
            serializer.instance,
            context=self.get_serializer_context()
        ).data, status=status.HTTP_201_CREATED, )


class GetPostApiView(generics.RetrieveAPIView):
    serializer_class = SpacePostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return SpacePost.objects.all()

    def get_object(self):
        return SpacePost.objects.get(id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        post = self.get_object()

        return Response(SpacePostSerializer(post, context=self.get_serializer_context()).data)


class SearchBlogPostsApiView(generics.ListAPIView):
    serializer_class = SpacePostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # parameters
        search_query = self.request.query_params.get('search', '')  # Retrieve 'search' query parameter

        return SpacePost.objects.filter(content__icontains= search_query)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        search_query = self.request.query_params.get('search', '')  # Retrieve 'search' query parameter

        # spaces = Space
        posts = []
        if user.is_authenticated and user.userRole == '2':
            posts = SpacePost.objects.filter(content__icontains=search_query)
        else :
            posts = SpacePost.objects.filter(content__icontains=search_query , space__allowed_user_types='public')
        return Response(SpacePostSerializer(posts, many=True, context={
            'request': self.request
        }).data)


class BlogSearchApiView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)


    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        blogs = Blog.objects.filter(title__icontains=search)
        return Response(BlogSerializer(blogs, many=True, context=self.get_serializer_context()).data)






# class SearchArticles
class SpacesSearch(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', '')  # Retrieve 'search' query parameter
        user = request.user
        spaces = []
        if user.is_authenticated and user.userRole == '2':
            spaces = Space.objects.filter(name__icontains=search_query)
        else:
            spaces = Space.objects.filter(name__icontains=search_query, allowed_user_types='public')
        return Response(RecommendedSpacesSerializer(spaces, many=True, context={
            'request': request
        }).data)



