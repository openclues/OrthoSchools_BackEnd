from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from useraccount.api.serializers.user_api_serializer import RegisterRequestSerializer, CreateProfileRequestSerializer, \
    CreateProfileResponseSerializer, ProfileFullDataSerializer
from useraccount.models import ProfileModel
from djoser.views import UserViewSet, TokenCreateView

# login even if the user is inactive

from djoser.views import TokenCreateView
from rest_framework.response import Response


class CustomTokenCreateView(TokenCreateView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Check user's active status here (customize as needed)

        token = Token.objects.create(user=user)
        # Include additional information in the response (e.g., user's active status)
        response_data = {
            'auth_token': token,
            'user_id': user.pk,
            'email': user.email,
            'is_active': user.is_active,
            # Include other user-related data as needed
        }

        return Response(response_data)


class RegisterApiView(UserViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegisterRequestSerializer

    def perfrom_create(self, serializer):
        print(self.serializer_class.fields)
        print("asdasdasdas")
        user = self.serializer_class.save(
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', '')
        )

    # def post(self, request, format=None):
    #     print(request.data)
    #     serializer = self.serializer_class(data=request.data)
    #     try:
    #         self.serializer_class.is_valid(raise_exception=True)
    #         user = UserAccount.objects.create_user(
    #             username=serializer.data['email'],
    #             email=serializer.data['email'],
    #             password=serializer.data['password'],
    #             first_name=serializer.data['first_name'],
    #             last_name=serializer.data['last_name']
    #         )
    #         messages.success(request, 'Signup successful! You are now logged in.')  # Add success message
    #         return Response(RegisterResponseSerializer(user, many=False).data, status=status.HTTP_201_CREATED)
    #     except serializers.ValidationError as e:
    #         return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


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
        serializer.validated_data['user_id'] = self.request.user.id
        serializer.save()


class UpdateUserAndProfileApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateProfileRequestSerializer

    def get_queryset(self):
        return ProfileModel.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj

    def perform_update(self, serializer):
        serializer.validated_data['user_id'] = self.request.user.id
        serializer.save()
        return Response(CreateProfileResponseSerializer(serializer.data, many=False).data, status=status.HTTP_200_OK)


class GetProfileApiView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileFullDataSerializer

    def get_queryset(self):
        return ProfileModel.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return Response(serializer.data)
