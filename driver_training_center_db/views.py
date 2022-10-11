from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from django.contrib.auth.models import User, Group, Permission
from rest_framework import viewsets, generics
from rest_framework import permissions
from driver_training_center_db.serializers import *


# class RoleViewSet(viewsets.ModelViewSet):
# 	"""
# 	API endpoint that allows roles to be viewed or edited.
# 	"""
# 	queryset = Role.objects.all()
# 	serializer_class = Role
# 	# permission_classes = [permissions.IsAuthenticated]
#
#
# class PermissionViewSet(viewsets.ModelViewSet):
# 	"""
# 	API endpoint that allows permissions to be viewed or edited.
# 	"""
# 	queryset = Permission.objects.all()
# 	serializer_class = PermissionSerializer
# 	# permission_classes = [permissions.IsAuthenticated]


class DrivingLicenseCategoryViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows driving license categories to be viewed or edited.
	"""
	queryset = DrivingLicenseCategory.objects.all()
	serializer_class = DrivingLicenseCategorySerializer
	# permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows courses to be viewed or edited.
	"""
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	# permission_classes = [permissions.IsAuthenticated]


class LessonViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows lessons to be viewed or edited.
	"""
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	# permission_classes = [permissions.IsAuthenticated]


class StudentCourseStatusViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows students' course statuses to be viewed or edited.
	"""
	# queryset = StudentCourseStatus.objects.filter(student=user)
	serializer_class = StudentCourseStatusSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			queryset = StudentCourseStatus.objects.all()
		else:
			queryset = StudentCourseStatus.objects.filter(student=user)
		return queryset


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class PermissionViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows permissions to be viewed or edited.
	"""
	queryset = Permission.objects.all()
	serializer_class = PermissionSerializer
	permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
