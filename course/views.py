from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course
from course.serializers import CourseSerializer


class CourseApiListView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        courses = Course.objects.all()
        return Response(CourseSerializer(courses, many=True).data)
