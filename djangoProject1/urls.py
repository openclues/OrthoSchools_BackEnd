"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from djoser.views import UserViewSet
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

import useraccount.websiteViews.views
from blog.views import BlogDetailView, BlogListView, FilteredArticlesListView, \
    LikeAndUnlikeArticle, BlogScreenView, BlogCreateAPIView, FollowUnfollowBlogApiView, CreateBlogPost, \
    GetArticlesByCategory, RecommendedBlogListView, GetArticleComments, CommentOnArticle, EditBlogView, ArticlesSearch
from commentable.views import GetSpacePostComments, MakeAreplayOnAComment, MakeBlogPostComment, GetSinglePostComment
from course.views import CourseApiListView
from djangoProject1 import settings
from notifications.views import RegisterDeviceView, RemoveFcmToken
from post.views import CreatePostApiView, GetPostApiView, SearchBlogPostsApiView, BlogSearchApiView, SpacesSearch
from saveditem.views import GetSaved, SaveAndUnsavePost
from space.models import Space
from space.serializers import ActivityViewSet
from space.views import UserSpacesListView, JoinSpaceApiView, LeaveSpaceApiView, SpaceRetrieveApiView, \
    GetRecommendedSpacesApiView, GetHomeSpacePostsApiView, GETSPACESANDBLOGSWITHCATEGORYNAME, LikeAndUnlikePost, \
    SpacePostsListView, FilterSpacesAndArticlesWithCategoryName, MakePostComment, MakeAreplyOnComment, \
    DiscoverPopularSpacesAndBlogs, LikeUnLikeReply, LikeAndUnlikeComment, UpdatePostComment
from useraccount.userViews import RegisterApiView, CreateProfileApiView, UpdateUserAndProfileApiView, \
    CustomTokenCreateView, GetProfileApiView, ProfileInterestsApiView, CategoriesApiView, HomeDataApiView, \
    ProfileViewSet, MyProfileViewSet, UserUpdateApiView, GetMySpaces, MyActivities, GenerateAndSendEmailCode, \
    VerifyEmailCode, GetUsersNoticiations, ViewNotification, SendPremiumRequest, UploadUserCardId, UploadCertificate, \
    UploadSelfie, RemoveCertificate, RemoveCardId, RemoveSelfie, CreateAverificationRequest, UploadProfileImage, \
    UpadateProfile, ChangePassword, SendCodeForResetPassword, ResetPassword, UploadCoverImage, MakePremium, \
    GetUsersListView, GetVerificationProRequestsForAdmin, ApproveOrDisApproveVerificationRequest, BIOupdateView, \
    SetPhoneNumberToVerified
from useraccount.websiteViews import profile_views

# from useraccount.websiteViews.views import signup_view
from useraccount.websiteViews.index_views import email_verification

router = DefaultRouter()

router.register(r'activity', ActivityViewSet, basename='activity')

urlpatterns = [
    # path('admin/', AdminHomeScreenView.as_view(), name='admin'),

    path('admin/', admin.site.urls, {'extra_context': {'spaces': Space.objects.all()}}),
    path('register/', RegisterApiView.as_view({'post': 'create'}), name='user-create'),
    path('visit/profile/<int:pk>', ProfileViewSet.as_view(), name='visit_profile'),
    # path('register/', RegisterApiView.as_view(), name='registeruser'),
    path('profile/create', CreateProfileApiView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('user/info', GetProfileApiView.as_view()),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('signup/', useraccount.websiteViews.views.register, name='signup'),
    # path('register/', useraccount.websiteViews.views.register, name='register'),
    path('login/', useraccount.websiteViews.views.login_view, name='login'),
    path('login_user/', useraccount.websiteViews.views.login_user, name='login_user'),
    path('', useraccount.websiteViews.views.IndexView, name='index'),
    path('logout/', useraccount.websiteViews.views.logout_view, name='logout'),
    # blog
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('activate/<str:uidb64>/<str:token>/', email_verification, name='email_verification'),
    path('profile/edit/', profile_views.ShowProfileView.as_view(), name='edit_profile'),
    path('profile/update/', UpdateUserAndProfileApiView.as_view(), name='update_profile'),
    path('update/interestes/', ProfileInterestsApiView.as_view(), name='update_interestes'),
    path('categories/', CategoriesApiView.as_view(), name='categories'),
    path('myspaces/', UserSpacesListView.as_view(), name='my_spaces'),
    path('homedata/', HomeDataApiView.as_view(), name='home_data'),
    path('register-device/', RegisterDeviceView.as_view(), name='register-device'),
    path('myactivities/', MyActivities.as_view(), name='my_activities'),
    path('joinspace/', JoinSpaceApiView.as_view(), name='join_space'),
    path('leavespace/', LeaveSpaceApiView.as_view(), name='leave_space'),
    path('postcreate/', CreatePostApiView.as_view(), name='create_post'),
    path('activity/', include(router.urls)),
    path('space/<int:pk>', SpaceRetrieveApiView.as_view(), name='space'),
    path('filter/category/', GETSPACESANDBLOGSWITHCATEGORYNAME.as_view(), name='filter_category'),
    path('post/<int:pk>', GetPostApiView.as_view(), name='get_post'),
    path('blogs/', BlogListView.as_view(), name='blogs'),
    path('article/', FilteredArticlesListView.as_view(), name='articles'),
    path('myprofile/', MyProfileViewSet.as_view(), name='my_profile'),
    # path('verify/pro', VerificationRequestViewSet.as_view(), name='send_verification_request'),
    path('update/profile', UserUpdateApiView.as_view(), name='update_profile'),
    path('update/bio/', BIOupdateView.as_view(), name='update_bio'),
    path('api/spaces/', GetMySpaces.as_view(), name='get_my_spaces'),
    path('api/recommended-spaces/', GetRecommendedSpacesApiView.as_view(), name='get_recommended_spaces'),
    path('api/recommended-blogs/', RecommendedBlogListView.as_view(), name='get_recommended_blogs'),
    path('api/home-posts/', GetHomeSpacePostsApiView.as_view(), name='get_home_posts'),
    path('api/post-comments/', GetSpacePostComments.as_view(), name='get_home_posts'),
    path('api/comment/<int:pk>', GetSinglePostComment.as_view(), name='get_single_comment'),
    path('api/post/comment', MakePostComment.as_view(), name='make_comment'),
    path('api/article/comment', MakeBlogPostComment.as_view(), name='make_comment_on_blog_post'),
    path('api/post/replay', MakeAreplyOnComment.as_view(), name='make_replay'),
    path('post/interact/', LikeAndUnlikePost.as_view(), name='like_and_unlike_post'),
    path('comment/interact/', LikeAndUnlikeComment.as_view(), name='like_and_unlike_comment'),
    path('article/interact/', LikeAndUnlikeArticle.as_view(), name='like_and_unlike_post'),
    path('space/posts/', SpacePostsListView.as_view(), name='space_posts'),
    path('sendemailcode/', GenerateAndSendEmailCode.as_view(), name='send_email_code'),
    path('verify/email/', VerifyEmailCode.as_view(), name='verify_email_code'),
    path('notifications/', GetUsersNoticiations.as_view(), name='get_notifications'),
    path('read/notification', ViewNotification.as_view(), name='read_notification'),
    path('saved', GetSaved.as_view(), name='get_saved'),
    path('save/post', SaveAndUnsavePost.as_view(), name='get_saved'),
    # path('api/article/comments/', GetBlogPostsComments.as_view(), name='token_obtain_pair'),
    path('get/blog/', BlogScreenView.as_view(), name='get_blog'),
    path('send/premium/', SendPremiumRequest.as_view(), name='send_premium_request'),
    path('send/premium/', MakeBlogPostComment.as_view(), name='send_premium_request'),
    path('blog/create', BlogCreateAPIView.as_view(), name='create_blog'),
    path('filter/', FilterSpacesAndArticlesWithCategoryName.as_view(),
         name='filter_spaces_and_articles_with_category_name'),
    path('blog/followunfollow/', FollowUnfollowBlogApiView.as_view(), name='follow_unfollow_blog'),
    path('courses/', CourseApiListView.as_view(), name='courses'),
    path('user/cardid/', UploadUserCardId.as_view(), name='upload_user_card_id'),
    path('user/certficate/', UploadCertificate.as_view(), name='upload_certificate'),
    path('article/comments/', GetArticleComments.as_view(), name='get_article_comments'),
    path('user/selfie/', UploadSelfie.as_view(), name='upload_selfie'),
    path('remove/certificate/', RemoveCertificate.as_view(), name='remove_certificate'),
    path('remove/cardId/', RemoveCardId.as_view(), name='remove_cardId'),
    path('remove/selfie/', RemoveSelfie.as_view(), name='remove_selfie'),
    path('send/verification/request', CreateAverificationRequest.as_view(), name='send_verification_request'),
    path('upload/profile/image', UploadProfileImage.as_view(), name='upload_profile_image'),
    path('upload/cover/image', UploadCoverImage.as_view(), name='upload_cover_image'),
    path('update/profile/', UpadateProfile.as_view(), name='yupdate_profile'),
    path('change/password/', ChangePassword.as_view(), name='change_password'),
    path('sendCodeForResetPassword/', SendCodeForResetPassword.as_view(), name='reset_password_code'),
    path('resetPassword/', ResetPassword.as_view(), name='reset_password'),
    path('create/article/', CreateBlogPost.as_view(), name='create_article'),
    path('article/comment/', CommentOnArticle.as_view(), name='comment_on_article'),
    path('discover/screen', DiscoverPopularSpacesAndBlogs.as_view(), name='discover_screen'),
    path('replay/interact/', LikeUnLikeReply.as_view(), name='replay_interact'),
    path('premieum/', MakePremium.as_view(), name='make_premieum'),
    path('read/articles/', GetArticlesByCategory.as_view(), name='read-articles'),
    path('search/posts/', SearchBlogPostsApiView.as_view(), name='search_posts'),
    path('search/articles/', ArticlesSearch.as_view(), name='search_articles'),
    path('search/spaces/', SpacesSearch.as_view(), name='search_spaces'),
    path('search/blogs/', BlogSearchApiView.as_view(), name='search_blogs'),
    path('manage/users/', GetUsersListView.as_view(), name='get_users'),
    path('blog/edit/', EditBlogView.as_view(), name='edit_blog'),
    path('unregister_device/', RemoveFcmToken.as_view(), name='unregister_device'),
    path('comment/update/', UpdatePostComment.as_view(), name='update_comment'),

    path('verificationsRequests/', GetVerificationProRequestsForAdmin.as_view(), name='get_verification_requests'),
    path('verificationRequest/interact/', ApproveOrDisApproveVerificationRequest.as_view(), name='approve_or_disapprove_verification_request'),
    path('verify/phone/', SetPhoneNumberToVerified.as_view(), name='verify_phone'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
