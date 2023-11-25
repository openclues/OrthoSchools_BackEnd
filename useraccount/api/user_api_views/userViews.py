from django.contrib import messages
from djoser import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.user_api_serializer import RegisterRequestSerializer, RegisterResponseSerializer, \
    CreateProfileResponseSerializer, CreateProfileRequestSerializer
from ...models import UserAccount, ProfileModel
from django.contrib.auth.hashers import make_password


class RegisterApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterRequestSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = UserAccount.objects.create_user(
                username=serializer.data['email'],
                email=serializer.data['email'],
                password=serializer.data['password'],
                first_name=serializer.data['first_name'],
                last_name=serializer.data['last_name']
            )
            messages.success(request, 'Signup successful! You are now logged in.')  # Add success message
            return Response(RegisterResponseSerializer(user, many=False).data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class CreateProfileApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateProfileRequestSerializer

    def get_queryset(self):
        return ProfileModel.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj

    def perform_update(self, serializer):
        # Set user_id before updating the instance
        serializer.validated_data['user_id'] = self.request.user.id
        serializer.save()
