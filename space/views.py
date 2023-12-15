from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Space
from .serializers import SpaceSerializer, JoinSpaceSerializer, LeaveSpaceSerializer

from django.shortcuts import render


# from rest_framework.serializers import
# Create your views here.


class UserSpacesListView(generics.ListAPIView):
    serializer_class = SpaceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Space.objects.filter(include_users=user)


class JoinSpaceApiView(generics.UpdateAPIView):
    serializer_class = JoinSpaceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Space.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, id=self.request.data.get('id'))
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'id': instance.id})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(SpaceSerializer(self.get_object(), many=False, context={'request': self.request}).data,
                        status=status.HTTP_200_OK, )


class LeaveSpaceApiView(generics.UpdateAPIView):
    serializer_class = LeaveSpaceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Space.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, id=self.request.data.get('id'))
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'id': instance.id})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response("", status=status.HTTP_204_NO_CONTENT)


class SpaceRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = SpaceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Space.objects.filter(include_users=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # serializer = self.get_serializer(instance, context={'request': self.request})
        return Response(SpaceSerializer(instance, many=False, context={'request': self.request}).data, )



