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
from blog.views import BlogDetailView, BlogListView
from djangoProject1 import settings
from post.views import CreatePostApiView, GetPostApiView
from space.models import Space
from space.serializers import ActivityViewSet
from space.views import UserSpacesListView, JoinSpaceApiView, LeaveSpaceApiView, SpaceRetrieveApiView
from useraccount.userViews import RegisterApiView, CreateProfileApiView, UpdateUserAndProfileApiView, \
    CustomTokenCreateView, GetProfileApiView, ProfileInterestsApiView, CategoriesApiView, HomeDataApiView, \
    ProfileViewSet
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
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('activate/<str:uidb64>/<str:token>/', email_verification, name='email_verification'),
    path('profile/edit/', profile_views.ShowProfileView.as_view(), name='edit_profile'),
    path('profile/update/', UpdateUserAndProfileApiView.as_view(), name='update_profile'),
    path('update/interestes/', ProfileInterestsApiView.as_view(), name='update_interestes'),
    path('categories/', CategoriesApiView.as_view(), name='categories'),
    path('myspaces/', UserSpacesListView.as_view(), name='my_spaces'),
    path('homedata/', HomeDataApiView.as_view(), name='home_data'),
    path('joinspace/', JoinSpaceApiView.as_view(), name='join_space'),
    path('leavespace/', LeaveSpaceApiView.as_view(), name='leave_space'),
    path('postcreate/', CreatePostApiView.as_view(), name='create_post'),
    path('activity/', include(router.urls)),
    path('space/<int:pk>', SpaceRetrieveApiView.as_view(), name='space'),
    path('post/<int:pk>', GetPostApiView.as_view(), name='get_post'),
    path('blogs/', BlogListView.as_view(), name='blogs'),

]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
