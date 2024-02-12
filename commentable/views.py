from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import BlogPost
from blog.views import PaginationList
from commentable.models import Comment
from commentable.serializers import CommentSerializer, CommentOnPostCreateSerializer
from likable.models import Like
from space.models import SpacePost, PostComment
from space.serializers import PostCommentSerializer


class GetSinglePostComment(generics.RetrieveAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PostComment.objects.all()

class GetSpacePostComments(generics.ListAPIView):
    serializer_class = PostCommentSerializer

    # pagination_class = PaginationList

    def get_queryset(self):
        post_id = self.request.query_params.get('id', None)
        post = SpacePost.objects.get(id=post_id)
        return post.comments.all()


class MakePostComment(generics.CreateAPIView):
    serializer_class = CommentOnPostCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        comment_content_type = ContentType.objects.get_for_model(SpacePost)
        commnet = Comment.objects.create(object_id=serializer.validated_data.get('object_id'),
                                         content_type=comment_content_type, user=self.request.user,
                                         text=serializer.validated_data.get('text'))
        commnet.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_content_type = ContentType.objects.get_for_model(SpacePost)
        comment = Comment.objects.create(
            object_id=serializer.validated_data.get('object_id'),
            content_type=comment_content_type,
            user=self.request.user,
            text=serializer.validated_data.get('text')
        )

        # Assuming AnotherSerializer is the serializer you want to use for the response
        another_serializer = CommentSerializer(comment)

        headers = self.get_success_headers(another_serializer.data)
        return Response(another_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MakeAreplayOnAComment(generics.CreateAPIView):
    serializer_class = CommentOnPostCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        comment_content_type = ContentType.objects.get_for_model(Comment)
        commnet = Comment.objects.create(object_id=serializer.validated_data.get('object_id'),
                                         content_type=comment_content_type, user=self.request.user,
                                         text=serializer.validated_data.get('text'))
        commnet.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_content_type = ContentType.objects.get_for_model(Comment)
        comment = Comment.objects.create(
            object_id=serializer.validated_data.get('object_id'),
            content_type=comment_content_type,
            user=self.request.user,
            text=serializer.validated_data.get('text')
        )

        # Assuming AnotherSerializer is the serializer you want to use for the response
        another_serializer = CommentSerializer(comment)

        headers = self.get_success_headers(another_serializer.data)
        return Response(another_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MakeBlogPostComment(APIView):
    serializer_class = CommentOnPostCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        comment_content_type = ContentType.objects.get_for_model(BlogPost)
        commnet = Comment.objects.create(object_id=serializer.validated_data.get('object_id'),
                                         content_type=comment_content_type, user=self.request.user,
                                         text=serializer.validated_data.get('text'))
        commnet.save()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_content_type = ContentType.objects.get_for_model(SpacePost)
        comment = Comment.objects.create(
            object_id=serializer.validated_data.get('object_id'),
            content_type=comment_content_type,
            user=self.request.user,
            text=serializer.validated_data.get('text')
        )

        # Assuming AnotherSerializer is the serializer you want to use for the response
        another_serializer = CommentSerializer(comment)

        return Response(another_serializer.data, status=status.HTTP_201_CREATED)


class LikeAndUnlikeComment(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        comment_id = request.query_params.get('comment_id', None)
        comment = Comment.objects.get(id=comment_id)

        if comment.likes.filter(
                user=request.user

        ).exists():
            like = Like.objects.get(
                user=request.user,
                object_id=comment_id,
                content_type=ContentType.objects.get_for_model(comment)
            )
            like.delete()
            return Response({"parent_likes_count": comment.likes.count(), 'message': 'unliked', 'isLiked': False},
                            status=status.HTTP_200_OK)



        else:
            like = Like.objects.create(
                user=request.user,
                object_id=comment_id,
                content_type=ContentType.objects.get_for_model(comment)
            )
            like.save()
            print(comment.likes.count())

            return Response({"parent_likes_count": comment.likes.count(), 'message': 'unliked', 'isLiked': True},
                            status=status.HTTP_200_OK)
