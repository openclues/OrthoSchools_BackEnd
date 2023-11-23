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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

import useraccount.websiteViews.views
from blog.views import BlogDetailView, AdminHomeScreenView
from djangoProject1 import settings
from useraccount.api.user_api_views.userViews import RegisterApiView, CreateProfileApiView

# from useraccount.websiteViews.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterApiView.as_view(), name='registeruser'),
    path('profile/create', CreateProfileApiView.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('signup/', useraccount.websiteViews.views.register, name='signup'),
    path('register/', useraccount.websiteViews.views.register, name='register'),
    path('login/', useraccount.websiteViews.views.login_view, name='login'),
    path('login_user/', useraccount.websiteViews.views.login_user, name='login_user'),
    path('', useraccount.websiteViews.views.IndexView, name='index'),
    path('logout/', useraccount.websiteViews.views.logout_view, name='logout'),
    # blog
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
