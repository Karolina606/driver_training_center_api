from rest_framework import viewsets, generics, permissions
from driver_training_center_db.serializers import *


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


class CourseStatusViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows students' course statuses to be viewed or edited.
	"""
	serializer_class = CourseStatusSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		if user.is_superuser:
			queryset = CourseStatus.objects.all()
		else:
			queryset = CourseStatus.objects.filter(student=user)
		return queryset


