from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from djangoProject1.firebase_services import FirebaseServices
from notifications.models import Message, Device
from notifications.serializers import MessageSerializer


class RegisterDeviceView(APIView):
    def post(self, request):
        user_id = request.user.id
        device_id = request.data.get('device_id')
        fcm_token = request.data.get('fcm_token')
        FirebaseServices.register_device_for_push_notification(user_id, device_id, fcm_token)
        return Response({'success': True})


# class MessagesListView(generics.ListAPIView):

class MarkAllMessagesRead(APIView):
    def post(self, request):
        user = request.user
        messages = Message.objects.filter(recipients__in=[user]).exclude(read_by__in=[user])
        for message in messages:
            message.read_by.add(user)
        return Response(status=status.HTTP_200_OK)


class GetAllMessages(generics.ListAPIView):
    permission_classes = []
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(recipients__in=[self.request.user])


class RemoveFcmToken(APIView):
    def post(self, request):
        user_id = request.user.id
        device_id = request.data.get('device_id')
        FirebaseServices.un_register_device_for_push_notification(user_id, device_id)
        return Response({'success': True})
