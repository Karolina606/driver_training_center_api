from django.contrib.auth.models import Group, Permission

from driver_training_center_db.models import *
from rest_framework import serializers


class DrivingLicenseCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DrivingLicenseCategory
        fields = ['url', 'name', 'theory_full_time', 'practice_full_time']


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['url', 'driving_license_category', 'start_date']


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lesson
        fields = ['url', 'instructor', 'course', 'type',
                  'start_date', 'end_date']


class CourseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStatus
        fields = ['url', 'student', 'course', 'paid_money',
                  'is_course_paid', 'is_internal_theoretical_exam_passed',
                  'is_internal_practical_exam_passed', 'lessons']

