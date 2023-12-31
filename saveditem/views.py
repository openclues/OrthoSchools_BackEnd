from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from post.serializers import SpacePostSerializer
from saveditem.models import SavedItem
from space.models import SpacePost


class GetSaved(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        savedItems = SavedItem.objects.filter(user=user, content_type=ContentType.objects.get_for_model(SpacePost))
        posts = SpacePost.objects.filter(id__in=savedItems.values_list('object_id', flat=True))
        return Response(SpacePostSerializer(posts, many=True, context={'request': self.request}).data)


class SaveAndUnsavePost(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = self.request.user
        post = SpacePost.objects.get(id=60)
        if SavedItem.objects.filter(user=user, object_id=post.id).exists():
            SavedItem.objects.filter(user=user, object_id=post.id).delete()
            return Response({'message': 'post unsaved'}, status=200)
        else:
            SavedItem.objects.create(user=user, object_id=post.id,
                                     content_type=ContentType.objects.get_for_model(SpacePost))
            return Response({'message': 'post saved'}, status=201)
