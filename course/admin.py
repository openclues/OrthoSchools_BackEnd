from django.contrib import admin

# Register your models here.
from course.models import Course


class CourseAdmin(admin.ModelAdmin):

    list_display = ('course_name', 'course_description', 'course_image', 'course_video', 'course_link')
    search_fields = ('course_name', 'course_description', 'course_image', 'course_video', 'course_link')


admin.site.register(Course, CourseAdmin)
