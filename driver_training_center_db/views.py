from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User, Group, Permission
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import UserGroupChecker, isInstructor
from driver_training_center_db.serializers import *


class DrivingLicenseCategoryViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows driving license categories to be viewed or edited.
	"""
	queryset = DrivingLicenseCategory.objects.all()
	serializer_class = DrivingLicenseCategorySerializer

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""
		if self.action in ('list', 'retrieve'):
			permission_classes = [permissions.IsAuthenticated]
		else:
			permission_classes = [permissions.IsAdminUser]
		return [permission() for permission in permission_classes]


class CourseViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows courses to be viewed or edited.
	"""
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		user = self.request.user
		queryset = None
		if user.is_superuser or UserGroupChecker.is_admin(user) or UserGroupChecker.is_instructor(user):
			queryset = Course.objects.all()
		elif UserGroupChecker.is_student(user):
			course_status = CourseStatus.objects.get(student=user)
			queryset = Course.objects.filter(course_status_for_student=course_status)
		return queryset

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""
		if self.action in ('list', 'retrieve', 'update', 'partial_update', 'destroy'):
			permission_classes = [permissions.IsAuthenticated]
		else:
			permission_classes = [permissions.IsAdminUser]
		return [permission() for permission in permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows lessons to be viewed or edited.
	"""
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		queryset = None
		user = self.request.user
		if user.is_superuser or UserGroupChecker.is_admin(user):
			queryset = Lesson.objects.all()
		elif UserGroupChecker.is_instructor(user):
			queryset = Lesson.objects.filter(instructor=user)
		elif UserGroupChecker.is_student(user):
			course_status = CourseStatus.objects.get(student=user)
			queryset = Lesson.objects.filter(lesson_course_status=course_status)
			print(queryset)
		return queryset

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""
		if self.action == 'retrieve':
			permission_classes = [permissions.IsAuthenticated]
		elif self.action in ('list', 'update', 'partial_update', 'destroy'):
			permission_classes = (permissions.IsAdminUser | isInstructor,)
		else:
			permission_classes = [permissions.DjangoModelPermissions]
		return [permission() for permission in permission_classes]


class CourseStatusViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows students' course statuses to be viewed or edited.
	"""
	serializer_class = CourseStatusSerializer

	def get_queryset(self):
		user = self.request.user
		queryset = None
		if user.is_superuser or UserGroupChecker.is_admin(user):
			queryset = CourseStatus.objects.all()
		elif UserGroupChecker.is_instructor(user):
			lessons_found = Lesson.objects.filter(instructor=user)
			course_statuses = []
			for lesson in lessons_found:
				for cs in CourseStatus.objects.all():
					if cs.lessons.contains(lesson):
						course_statuses.append(cs)
			course_statuses_id = [cs.id for cs in course_statuses]
			queryset = CourseStatus.objects.filter(id__in=course_statuses_id)
		elif UserGroupChecker.is_student(user):
			queryset = CourseStatus.objects.filter(student=user)
		return queryset

	@action(detail=True, methods=['put'], name='add_lesson_to_stu_course')
	def add_lesson_to_stu_course(self, request, pk=None, *args, **kwargs):
		course_status = CourseStatus.objects.get(id=pk)
		lesson = Lesson.objects.get(id=int(kwargs['lesson']))

		course_status.lessons.add(lesson)
		course_status.save()
		return Response()

	@action(detail=True, methods=['get'], name='get_by_lesson_id')
	def get_by_lesson_id(self, request, pk=None):
		if UserGroupChecker.is_student(request.user):
			student_id = User.objects.get(username=request.user).id
			data = CourseStatus.objects.filter(lessons=pk).values().filter(student_id=student_id)
		else:
			data = CourseStatus.objects.filter(lessons=pk).values()
		return Response(data)

	@action(detail=True, methods=['get'], name='get_by_course_id')
	def get_by_course_id(self, request, pk=None):
		data = CourseStatus.objects.filter(course_id=pk).values()
		return Response(data)

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""
		if self.action == 'retrieve':
			permission_classes = [permissions.IsAuthenticated]
		elif self.action in ('list', 'get_by_lesson_id', 'update', 'partial_update', 'destroy' 'add_lesson_to_stu_course', 'get_by_course_id'):
			permission_classes = (permissions.IsAdminUser | isInstructor,)
		else:
			permission_classes = [permissions.IsAdminUser]
		return [permission() for permission in permission_classes]
