from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models.functions import Coalesce, Greatest
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer
from blog.views import PaginationList
from commentable.models import Comment
from likable.models import Like
from post.serializers import SpacePostSerializer
from useraccount.models import Category
from useraccount.serializers import RecommendedSpacesSerializer
from .models import Space, SpacePost
from .serializers import SpaceSerializer, JoinSpaceSerializer, LeaveSpaceSerializer, SimpleSpaceSerializer
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


class JoinSpaceApiView(APIView):
    # serializer_class = JoinSpaceSerializer
    permission_classes = (IsAuthenticated,)

    def post (self, request):
        space_id = request.query_params.get('space_id', None)
        space = Space.objects.get(id=space_id)
        if space.is_allowed_to_join(space, request.user):
            space.include_users.add(request.user)
            return Response( SimpleSpaceSerializer (space, many=False, context={'request': self.request}).data,
                            status=status.HTTP_200_OK, )
        else:
            return Response({"message": "You are not allowed to join this space"},
                            status=status.HTTP_400_BAD_REQUEST, )


    # serializer_class = JoinSpaceSerializer
    # permission_classes = (IsAuthenticated,)
    #
    # def get_queryset(self):
    #     return Space.objects.all()
    #
    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = generics.get_object_or_404(queryset, id=4)
    #     return obj
    #
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data={'id': instance.id})
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(SpaceSerializer(self.get_object(), many=False, context={'request': self.request}).data,
    #                     status=status.HTTP_200_OK, )


# class JoinSpace(ApiView):

class LeaveSpaceApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        space_id = request.query_params.get('space_id', None)
        space = Space.objects.get(id=space_id)
        space.include_users.remove(request.user)
        return Response(SimpleSpaceSerializer(space, many=False, context={'request': self.request}).data,
                        status=status.HTTP_200_OK, )


# class GetSpace(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         space_id = request.query_params.get('space_id', None)
#         space = Space.objects.get(id=space_id)
#         return Response(SpaceSerializer(space, many=False, context={'request': self.request}).data)


class SpaceRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = RecommendedSpacesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Space.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
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
        return SpacePost.objects.all()


class GETSPACESANDBLOGSWITHCATEGORYNAME(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category_id = request.query_params.get('category_id', None)
        spaces = Space.objects.filter(
            category__in=[category_id]
        )
        category = Category.objects.get(id=category_id)
        spaces_serializer = RecommendedSpacesSerializer(spaces, many=True, context={'request': self.request}).data
        blogs = Blog.objects.filter(
            category__in=[category_id]
        )
        blogsSerializer = BlogSerializer(blogs, many=True, context={'request': self.request}).data
        return Response({'spaces': spaces_serializer, 'blogs': blogsSerializer})


class LikeAndUnlikePost(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        post_id = request.query_params.get('post_id', None)
        post = SpacePost.objects.get(id=post_id)
        if post.likes.filter(
                user=request.user

        ).exists():
            like = Like.objects.get(
                user=request.user,
                object_id=post_id,
                content_type=ContentType.objects.get_for_model(post)
            )
            like.delete()

            return Response({"parent_likes_count": post.likes.count(), 'message': 'unliked', 'isLiked': False},
                            status=status.HTTP_200_OK)

        else:
            like = Like.objects.create(
                user=request.user,
                object_id=post_id,
                content_type=ContentType.objects.get_for_model(post)
            )
            like.save()
            return Response({"parent_likes_count": post.likes.count(), 'message': 'liked', 'isLiked': True},
                            status=status.HTTP_200_OK)

# filter posts according to recent, popular, most commented
class FilterPosts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        filter = request.query_params.get('filter', None)
        if filter == 'recent':
            posts = SpacePost.objects.all().order_by('-created_at')
        elif filter == 'popular':
            posts = SpacePost.objects.all().annotate(
                likes_count=Coalesce(Max('likes__id'), Value(0)),
                comments_count=Coalesce(Max('comments__id'), Value(0))
            ).order_by('-likes_count')
        elif filter == 'most_commented':
            posts = SpacePost.objects.all().annotate(
                likes_count=Coalesce(Max('likes__id'), Value(0)),
                comments_count=Coalesce(Max('comments__id'), Value(0))
            ).order_by('-comments_count')
        else:
            posts = SpacePost.objects.all().order_by('-created_at')
        return Response(SpacePostSerializer(posts, many=True, context={'request': self.request}).data)


class SpacePostsListView(generics.ListAPIView):
    serializer_class = SpacePostSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PaginationList

    # sort
    # filter

    def get_queryset(self):
        space_id = self.request.query_params.get('id', None)
        if space_id is None:
            return SpacePost.objects.all()
        else:
            filter = self.request.query_params.get('filter', None)
            if filter == 'recent':

                return SpacePost.objects.filter(space=space_id).order_by('-created_at')

            elif filter == 'popular':
                return SpacePost.objects.filter(space=space_id).annotate(
                    likes_count=Coalesce(Max('likes__id'), Value(0)),
                    comments_count=Coalesce(Max('comments__id'), Value(0))
                ).order_by('-likes_count')
            elif filter == 'most_commented':
                return SpacePost.objects.filter(space=space_id).annotate(
                    likes_count=Coalesce(Max('likes__id'), Value(0)),
                    comments_count=Coalesce(Max('comments__id'), Value(0))
                ).order_by('-comments_count')
            else:
                return SpacePost.objects.filter(space=space_id).order_by('-created_at')








class FilterSpacesAndArticlesWithCategoryName(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        category_id = request.query_params.get('category_id', None)
        spaces = Space.objects.filter(
            category__in=[category_id]
        )
        category = Category.objects.get(id=category_id)
        spaces_serializer = RecommendedSpacesSerializer(spaces, many=True, context={'request': self.request}).data
        blogs = Blog.objects.filter(
            category__in=[category_id]
        )
        blogsSerializer = BlogSerializer(blogs, many=True, context={'request': self.request}).data
        return Response({'spaces': spaces_serializer, 'blogs': blogsSerializer})