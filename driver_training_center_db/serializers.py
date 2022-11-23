from datetime import datetime as dt, timedelta

from rest_framework.serializers import raise_errors_on_nested_writes

from driver_training_center_db.models import *
from rest_framework import serializers


class DrivingLicenseCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DrivingLicenseCategory
        fields = ['url', 'id', 'name', 'theory_full_time', 'practice_full_time']
        extra_kwargs = {
            'name': {'required': False},
            'theory_full_time': {'required': False},
            'practice_full_time': {'required': False}
        }

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['url', 'id', 'driving_license_category', 'start_date']
        extra_kwargs = {
            'driving_license_category': {'required': False},
            'start_date': {'required': False}
        }

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['url', 'id', 'instructor', 'course', 'type',
                  'start_date', 'end_date']
        extra_kwargs = {
            'instructor': {'required': False},
            'course': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False}
        }

    def validate(self, attrs):
        delta = attrs['end_date'] - attrs['start_date']
        if attrs['start_date'] > attrs['end_date'] or delta > timedelta(hours=6):
            raise serializers.ValidationError(
                {"End date must be past start_date."})
        return attrs

    def create(self, validated_data):
        instructor = self.validated_data['instructor']
        if instructor.groups.filter(name='instructor').exists():
            lesson = Lesson(
                course=self.validated_data['course'],
                instructor=self.validated_data['instructor'],
                type=self.validated_data['type'],
                start_date=self.validated_data['start_date'],
                end_date=self.validated_data['end_date'],
            )
            lesson.save()
            return lesson
        else:
            raise Exception('Instructor must be in group of instructor')

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class CourseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStatus
        fields = ['url', 'id', 'student', 'course', 'paid_money',
                  'is_course_paid', 'is_internal_theoretical_exam_passed',
                  'is_internal_practical_exam_passed', 'lessons']
        extra_kwargs = {
            'student': {'required': False},
            'course': {'required': False},
            'paid_money': {'required': False},
            'is_course_paid': {'required': False},
            'is_internal_theoretical_exam_passed': {'required': False},
            'is_internal_practical_exam_passed': {'required': False},
            'lessons': {'required': False}
        }

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

