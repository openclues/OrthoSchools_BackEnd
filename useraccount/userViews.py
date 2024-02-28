from actstream.models import Action
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from djangoProject1 import settings
from djangoProject1.send_notification_service import SendNotificationService
from home.serializers import HomeDataSerializer
from notifications.models import Message
from notifications.serializers import MessageSerializer
from space.models import Space
from space.serializers import ActivitySerializer
from useraccount.api.serializers.user_api_serializer import RegisterRequestSerializer, CreateProfileRequestSerializer, \
    CreateProfileResponseSerializer, ProfileFullDataSerializer, ProfileInterestesSerializer, CategorySerializer
from useraccount.models import ProfileModel, Category, UserAccount, PremiumRequest, Certificate, VerificationProRequest, \
    Premium
from djoser.views import UserViewSet, TokenCreateView

# login even if the user is inactive

from djoser.views import TokenCreateView
from rest_framework.response import Response

from useraccount.serializers import FullUserSerializer, VisitorProfileSerializer, \
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
            user.is_active = True
            user.email_verification_code = None
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Wrong code'}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersNoticiations(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def get_queryset(self):
        messages = Message.objects.filter(recipients__in=[self.request.user]).order_by('-created_at')
        print(len(messages))
        return messages


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


class UploadUserCardId(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user

        # Check if 'cardId' is in the uploaded files
        if 'cardId' in request.FILES:
            user.profilemodel.id_card = request.FILES['cardId']
            print(user.profilemodel.id_card)
            user.profilemodel.save()
            return Response({'message': 'Card Id image uploaded successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Card Id image not found in the request'}, status=status.HTTP_400_BAD_REQUEST)


class UploadCertificate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user

        # Check if 'cardId' is in the uploaded files
        if 'certificate' in request.FILES:

            crt = Certificate.objects.create(profile=user.profilemodel, certificateFile=request.FILES['certificate'],
                                             title=str(request.FILES['certificate']))
            return Response({'certificate': crt.title}, status=status.HTTP_200_OK)
            # user.profilemodel.certificate = request.FILES['certificate']
            # print(user.profilemodel.certificate)
        else:
            return Response({'message': 'Certificate not found in the request'}, status=status.HTTP_400_BAD_REQUEST)


class UploadSelfie(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user

        # Check if 'cardId' is in the uploaded files
        if 'selfie' in request.FILES:
            user.profilemodel.selfie = request.FILES['selfie']
            print(user.profilemodel.selfie)
            user.profilemodel.save()
            return Response({'message': 'Selfie image uploaded successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Selfie image not found in the request'}, status=status.HTTP_400_BAD_REQUEST)


# class SearchSpacesBlogsPostsArticles(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, *args, **kwargs):
#         # Assuming your User model has a 'card_id_image' field
#         user = self.request.user
#         query = request.query_params.get('query', None)
#         if query is None:
#             return Response({'message': 'query is required'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             spaces = Space.objects.filter(name__icontains=query)
#             blogs = Blog.objects.filter(title__icontains=query)
#             posts = BlogPost.objects.filter(title__icontains=query)
#             articles = Article.objects.filter(title__icontains=query)
#             return Response({'spaces': SpaceSerializerJustName(spaces, many=True).data,
#                              'blogs': BlogSerializerJustName(blogs, many=True).data,
#                              'posts': BlogPostSerializerJustName(posts, many=True).data,
#                              'articles': ArticleSerializerJustName(articles, many=True).data,
#                              }, status=status.HTTP_200_OK


class RemoveCertificate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user
        certificate_id = request.data.get('certificate_id', None)
        if certificate_id is None:
            return Response({'message': 'certificate_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            certificate = Certificate.objects.get(id=certificate_id)
            certificate.delete()
            return Response({'message': 'Certificate deleted successfully'}, status=status.HTTP_200_OK)


class RemoveCardId(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user
        user.profilemodel.id_card = None
        user.profilemodel.save()
        return Response({'message': 'Card Id deleted successfully'}, status=status.HTTP_200_OK)


class RemoveSelfie(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user
        user.profilemodel.selfie = None
        user.profilemodel.save()
        return Response({'message': 'Selfie deleted successfully'}, status=status.HTTP_200_OK)


class CreateAverificationRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user
        VerificationProRequest.objects.create(profile=user.profilemodel)
        return Response({'message': 'Verification request sent successfully'}, status=status.HTTP_200_OK)


class UploadProfileImage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user

        # Check if 'cardId' is in the uploaded files
        if 'profileImage' in request.FILES:
            user.profilemodel.profileImage = request.FILES['profileImage']
            print(user.profilemodel.profileImage)
            user.profilemodel.save()
            return Response({'message': 'Profile image uploaded successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Profile image not found in the request'}, status=status.HTTP_400_BAD_REQUEST)


class UploadCoverImage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # Assuming your User model has a 'card_id_image' field
        user = self.request.user

        # Check if 'cardId' is in the uploaded files
        if 'coverImage' in request.FILES:
            user.profilemodel.cover = request.FILES['coverImage']
            print(user.profilemodel.cover)
            user.profilemodel.save()
            return Response({'message': 'Cover image uploaded successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Cover image not found in the request'}, status=status.HTTP_400_BAD_REQUEST)


class UpadateProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        title = request.data.get('title', None)
        bio = request.data.get('bio', None)
        place_of_work = request.data.get('place_of_work', None)
        country = request.data.get('country', None)
        city = request.data.get('city', None)
        state = request.data.get('state', None)
        speciality = request.data.get('speciality', None)
        study_in = request.data.get('study_in', None)
        phone = request.data.get('phone', None)
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)

        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.save()
        user.profilemodel.title = title
        user.profilemodel.bio = bio
        user.profilemodel.place_of_work = place_of_work
        user.profilemodel.speciality = speciality
        user.profilemodel.study_in = study_in
        user.profilemodel.save()

        return Response(FullUserSerializer(
            user.profilemodel, many=False, context={'request': self.request}).data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        old_password = request.data.get('old_password', None)
        new_password = request.data.get('new_password', None)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)


class SendCodeForResetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        user = UserAccount.objects.get(email=email)

        if user is not None:
            try:
                user.generate_email_verification_code()
                user.send_email_verification()
                return Response({'message': 'Code sent successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Wrong email'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        code = request.data.get('code', None)
        password = request.data.get('password', None)
        user = UserAccount.objects.get(email=email)

        if user is not None:
            if code == user.email_verification_code:
                user.email_verified = True
                user.email_verification_code = None
                user.set_password(password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Wrong code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Wrong email'}, status=status.HTTP_400_BAD_REQUEST)


class MakePremium(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        full_name = request.data.get('full_name', None)
        phone = request.data.get('phone', None)
        email = request.data.get('email', None)
        clinic_name = request.data.get('clinic_name', None)
        clinic_address = request.data.get('clinic_address', None)
        profissional_title = request.data.get('professional_title', "Dr")
        license_number = request.data.get('license_number', None)
        education = request.data.get('education', None)
        graduation_year = request.data.get('graduation_year', None)
        certifications = request.data.get('certifications', None)
        experience = request.data.get('experience', None)

        Premium.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone,
            email_address=email,
            license_number=license_number,
            professional_title=profissional_title,
            clinic_name=clinic_name,
            clinic_address=clinic_address,
            education=education,
            graduation_year=graduation_year,
            certifications=certifications,
            experience=experience

        )

        return Response({'message': 'Premium request sent successfully'}, status=status.HTTP_200_OK)


class GetUsersListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # if user in a group:

    serializer_class = FullUserSerializer
    queryset = ProfileModel.objects.all()

    def get_queryset(self):
        return ProfileModel.objects.all()

    def get(self, request, *args, **kwargs):
        # param
        search = request.query_params.get('search', None)
        if request.user.groups.filter(name__contains='users').exists():
            if search is not None:
                # search for name or email or phone number
                users = ProfileModel.objects.filter(user__first_name__icontains=search) | ProfileModel.objects.filter(
                    user__last_name__icontains=search) | ProfileModel.objects.filter(
                    user__email__icontains=search) | ProfileModel.objects.filter(user__phone__icontains=search)
                return Response(FullUserSerializer(users, many=True, context={
                    'request': request
                }).data, status=status.HTTP_200_OK)
            else:
                users = ProfileModel.objects.all()
                return Response(FullUserSerializer(users, many=True,
                                                   context={
                                                       'request': request
                                                   }
                                                   ).data, status=status.HTTP_200_OK)


class GetVerificationProRequestsForAdmin(APIView):
    permission_classes = (IsAuthenticated,)

    # if user in a group:

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name__contains=settings.VERIFICATIONREQUESTS).exists():
            requests = VerificationProRequest.objects.filter(requestStatus='pending')
            return Response(VerifyUserSerializer(requests, many=True, context={
                'request': request
            }).data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not allowed to access this resource'},
                            status=status.HTTP_403_FORBIDDEN)


class ApproveOrDisApproveVerificationRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name__contains=settings.VERIFICATIONREQUESTS).exists():
            request_id = request.data.get('request_id', None)
            requeestStatus = request.data.get('status', None)
            if request_id is None:
                return Response({'message': 'request_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                request = VerificationProRequest.objects.get(id=request_id)
                if requeestStatus == 'approved':
                    request.requestStatus = 'approved'
                    UserAccount.objects.filter(id=request.profile.user.id).update(
                        is_verified_pro=True
                    )
                    request.save()
                    SendNotificationService.seneMessagewithPaylod(
                        title='Verification Request',
                        message='Your verification request has been approved',
                        recipients=[request.profile.user.id],
                        data={
                            'type': 'verification',
                        }

                    )
                    return Response({'message': 'Request approved successfully'}, status=status.HTTP_200_OK)
                elif requeestStatus == 'rejected':
                    request.requestStatus = 'rejected'
                    request.save()
                    UserAccount.objects.filter(id=request.profile.user.id).update(
                        is_verified_pro=False
                    )
                    SendNotificationService.seneMessagewithPaylod(
                        title='Verification Request',
                        message='Your verification request has been rejected',
                        recipients=[request.profile.user.id],
                        data={
                            'type': 'verification',
                        }
                    )
                    return Response({'message': 'Request rejected successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'status is required'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not allowed to access this resource'},
                            status=status.HTTP_403_FORBIDDEN)
