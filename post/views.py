from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from post.serializers import AddPostSerializer, SpacePostSerializer
from space.models import SpacePost


class CreatePostApiView(generics.CreateAPIView):
    serializer_class = AddPostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        print(serializer.instance)
        print(self.request.data)
        post_images = self.request.FILES.getlist('post_images')

        for image in post_images:
            print(image)
            serializer.instance.post_images.create(image=image)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(SpacePostSerializer(
            serializer.instance,
            context=self.get_serializer_context()
        ).data, status=status.HTTP_201_CREATED, headers=headers, )


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
