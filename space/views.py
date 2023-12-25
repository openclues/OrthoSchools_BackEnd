from django.db.models.functions import Coalesce, Greatest
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blog.views import PaginationList
from post.serializers import SpacePostSerializer
from useraccount.serializers import RecommendedSpacesSerializer
from .models import Space, SpacePost
from .serializers import SpaceSerializer, JoinSpaceSerializer, LeaveSpaceSerializer
from django.db.models import F, Max, Value, DateTimeField

from django.shortcuts import render


# from rest_framework.serializers import
# Create your views here.


class UserSpacesListView(generics.ListAPIView):
    serializer_class = RecommendedSpacesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        id = self.request.query_params.get('id', None)
        print("dfsfdf")
        if id is None:
            return Space.objects.filter(include_users=self.request.user)
        else:
            return Space.objects.filter(include_users=id)


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
    serializer_class = RecommendedSpacesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Space.objects.filter(include_users=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # serializer = self.get_serializer(instance, context={'request': self.request})
        return Response(RecommendedSpacesSerializer(instance, many=False, context={'request': self.request}).data, )


class GetRecommendedSpacesApiView(generics.ListAPIView):
    serializer_class = RecommendedSpacesSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PaginationList

    def get_queryset(self):
        user = self.request.user
        return Space.objects.order_by('?').exclude(include_users=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': self.request})
        return Response(serializer.data)


class GetHomeSpacePostsApiView(generics.ListAPIView):
    serializer_class = SpacePostSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PaginationList

    def get_queryset(self):
        user = self.request.user
        return SpacePost.objects.all() \
            .annotate(
            max_date=Coalesce(Max('comments__created_at'), Max('created_at'), Value('1970-01-01'),
                              output_field=DateTimeField()
                              )).order_by('-max_date')
