from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blog.views import PaginationList
from commentable.models import Comment
from commentable.serializers import CommentSerializer
from space.models import SpacePost


class GetSpacePostComments(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = PaginationList

    def get_queryset(self):
        post_id = self.request.query_params.get('id', None)
        post = SpacePost.objects.get(id=post_id)
        return post.comments.all()
