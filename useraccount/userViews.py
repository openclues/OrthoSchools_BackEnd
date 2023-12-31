from actstream.models import Action
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Message
from notifications.serializers import MessageSerializer
from space.models import Space
from space.serializers import ActivitySerializer
from useraccount.api.serializers.user_api_serializer import RegisterRequestSerializer, CreateProfileRequestSerializer, \
    CreateProfileResponseSerializer, ProfileFullDataSerializer, ProfileInterestesSerializer, CategorySerializer
from useraccount.models import ProfileModel, Category, UserAccount, PremiumRequest
from djoser.views import UserViewSet, TokenCreateView

# login even if the user is inactive

from djoser.views import TokenCreateView
from rest_framework.response import Response

from useraccount.serializers import HomeDataSerializer, FullUserSerializer, VisitorProfileSerializer, \
    VerifyUserSerializer, UserUpdateSerializer, SpaceSerializerJustName, RecommendedSpacesSerializer, \
    EmailVerificationSerializer


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
        # handle the interests
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
        return Response(ProfileFullDataSerializer(serializer.data, many=False).data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        user = self.get_object()
        serialized_data = FullUserSerializer(user, many=False, context={'request': self.request}).data
        return Response(serialized_data, status=status.HTTP_200_OK)


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


class ProfileInterestsApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileInterestesSerializer

    def get_queryset(self):
        return ProfileModel.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj


class CategoriesApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # pass context to the serializer
    def get_serializer_context(self):
        return {'request': self.request}


class HomeDataApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # Assuming you want to get home data for the currently authenticated user
        user = self.request.user

        # You can add any additional logic or customization here before serializing the data
        serializer = HomeDataSerializer({'user': user}, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(generics.RetrieveAPIView):
    serializer_class = FullUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ProfileModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = ProfileModel.objects.get(user_id=kwargs['pk'])
        serializer = FullUserSerializer(instance, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)


class MyProfileViewSet(generics.RetrieveAPIView):
    serializer_class = FullUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ProfileModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = ProfileModel.objects.get(user_id=request.user.id)
        serializer = FullUserSerializer(instance, context={'request': request})
        print(serializer.data)
        return Response(serializer.data)


# class VerificationRequestViewSet(generics.CreateAPIView):
#     serializer_class = VerifyUserSerializer
#     permission_classes = (IsAuthenticated,)
#     queryset = ProfileModel.objects.all()


class UserUpdateApiView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = UserAccount.objects.all()

    def get_object(self):
        print(self.request.user)
        queryset = self.get_queryset()
        obj = UserAccount.objects.get(id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        try:
            serializer.save()
            user = self.get_object()
            serialized_data = FullUserSerializer(user.profilemodel, many=False, context={'request': self.request}).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error during update: {e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        full_user_serializer = FullUserSerializer(user.profilemodel, many=False, context={'request': self.request})

        return Response(full_user_serializer.data, status=status.HTTP_200_OK)


class GetMySpaces(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecommendedSpacesSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        # get id from the url params
        id = self.lookup_url_kwarg
        print(id)

        if id is None:
            return Space.objects.filter(include_users=self.request.user)
        else:
            return Space.objects.filter(include_users=id)

    def get_object(self):
        id = self.kwargs.get('id', None)
        print(id)

        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj

    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs.get('id', None)
        print(id)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return Response(serializer.data)


class MyActivities(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivitySerializer

    def get_queryset(self):
        return Action.objects.filter(actor_object_id=self.request.user.id).order_by('-timestamp')


class GenerateAndSendEmailCode(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user.generate_email_verification_code()
        # try catch

        try:
            user.send_email_verification()
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyEmailCode(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code', None)
        if code is None:
            return Response({'message': 'code is required'}, status=status.HTTP_400_BAD_REQUEST)
        if code == user.email_verification_code:
            user.email_verified = True
            user.email_verification_code = None
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Wrong code'}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersNoticiations(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(recipients__in=[self.request.user]).order_by('-created_at')


class ViewNotification(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        notification_id = request.query_params.get('notification_id', None)
        notification = Message.objects.get(id=notification_id)
        notification.read_by.add(request.user)
        notification.save()
        return Response({'message': 'Notification viewed successfully'}, status=status.HTTP_200_OK)


class SendPremiumRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.userRole == 2:
            return Response({'message': 'You are already a premium user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if PremiumRequest.objects.filter(
                    profile=user.profilemodel).filter(requestStatus='pending').filter(
            ).exists():
                return Response({'message': 'You already have a pending request'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                PremiumRequest.objects.create(profile=user.profilemodel)
                return Response({'message': 'Request sent successfully'}, status=status.HTTP_200_OK)
