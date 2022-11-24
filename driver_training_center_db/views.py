import datetime
import http

from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User, Group, Permission
from rest_framework.decorators import action
from rest_framework.response import Response
import django.http

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
			course_statuses = CourseStatus.objects.filter(student=user)
			queryset = Course.objects.filter(course_status_for_student__in=course_statuses)
		return queryset.order_by('-start_date')

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
			course_statuses = CourseStatus.objects.filter(student=user)
			queryset = Lesson.objects.filter(lesson_course_status__in=course_statuses)
		queryset = queryset.filter(end_date__gte=(datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60)))
		return queryset.order_by('start_date')

	@action(detail=False, methods=['get'], name='get_ended_lessons')
	def get_ended_lessons(self, request):
		if UserGroupChecker.is_student(request.user):
			course_statuses = CourseStatus.objects.filter(student=request.user)
			data = Lesson.objects.filter(lesson_course_status__in=course_statuses)
		elif UserGroupChecker.is_instructor(request.user):
			instructor_id = User.objects.get(username=request.user).id
			data = Lesson.objects.filter(instructor_id=instructor_id)
		else:
			data = Lesson.objects.all()
		data = data.order_by('-start_date').filter(
			end_date__lt=(datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60))).values()
		return Response(data)

	# "instructor": instructor,
	# "course": course,
	# "type": type,
	# "start_date": formatData(startDate),
	# "end_date": formatData(endDate)

	@action(detail=False, methods=['post'], name='add_lesson_with_students')
	def add_lesson_with_students(self, request):
		print(request.data)
		print('######')

		lesson = Lesson(
				instructor=User.objects.get(id=request.data['instructor']),
				course=Course.objects.get(id=request.data['course']),
				type=request.data['type'],
				start_date=datetime.datetime.strptime(request.data['start_date'], '%Y-%m-%dT%H:%M:%SZ'),
				end_date=datetime.datetime.strptime(request.data['end_date'], '%Y-%m-%dT%H:%M:%SZ')
			)

		if request.data['type'] == 'P' and len(request.data['students']) > 1:
			# return Response({"status": str(http.HTTPStatus.BAD_REQUEST), 'message': 'Cannot add many students to practice lesson'})
			raise Exception('Cannot add many students to practice lesson')

		if is_meeting_interfering(User.objects.get(id=request.data['instructor']), lesson):
			raise Exception('Meeting interferes with instructor plans')

		for student_status_id in request.data['students']:
			student = CourseStatus.objects.get(id=student_status_id).student
			if is_meeting_interfering(student, lesson):
				raise Exception('Meeting interferes with student plans')

		lesson.save()

		for student_status_id in request.data['students']:
			status = CourseStatus.objects.get(id=student_status_id)
			status.lessons.add(lesson)
			status.save()

		return Response(http.HTTPStatus.CREATED)

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""
		if self.action in ('retrieve', 'get_ended_lessons'):
			permission_classes = [permissions.IsAuthenticated]
		elif self.action in ('list', 'update', 'partial_update', 'destroy', 'add_lesson_with_students'):
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
		return queryset.order_by('-id')

	@action(detail=True, methods=['put'], name='add_lesson_to_stu_course')
	def add_lesson_to_stu_course(self, request, pk=None, *args, **kwargs):
		course_status = CourseStatus.objects.get(id=pk)
		lesson = Lesson.objects.get(id=int(kwargs['lesson']))

		course_status.lessons.add(lesson)
		course_status.save()
		return Response()

	@action(detail=True, methods=['delete'], name='delete_lesson_from_stu_course')
	def delete_lesson_from_stu_course(self, request, pk=None, *args, **kwargs):
		course_status = CourseStatus.objects.get(id=pk)
		lesson = Lesson.objects.get(id=int(kwargs['lesson']))

		try:
			course_status.lessons.remove(lesson)
			course_status.save()
			return Response(status=203)
		except:
			return Response(status=500)

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

	@action(detail=True, methods=['get'], name='get_progress')
	def get_progress(self, request, pk=None):
		data = {'theory': 0, 'practice': 0, 'theory_perc': 0, 'practice_perc': 0}

		course_status = CourseStatus.objects.get(id=pk)
		course = Course.objects.get(id=course_status.course_id)
		category = DrivingLicenseCategory.objects.get(id=course.driving_license_category.id)

		print(datetime.datetime.now())

		all_theory_lessons = Lesson.objects.filter(lesson_course_status=course_status, type='T',
													end_date__lt=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60))
		all_practice_lessons = Lesson.objects.filter(lesson_course_status=course_status, type='P',
													end_date__lt=datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60))

		for lesson in all_theory_lessons:
			print(lesson)
			data['theory'] += (lesson.end_date - lesson.start_date).seconds // 3600
			print("data_theory " + str(data['theory']))

		for lesson in all_practice_lessons:
			print(lesson)
			data['practice'] += (lesson.end_date - lesson.start_date).seconds // 3600
			print("data_practice " + str(data['practice']))

		data['theory_perc'] = data['theory'] / float(category.theory_full_time) * 100.0
		data['practice_perc'] = data['practice'] / float(category.practice_full_time) * 100.0
		return Response(data)

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""

		if self.action in ('retrieve', 'get_progress'):
			permission_classes = [permissions.IsAuthenticated]
		elif self.action in (
				'list', 'get_by_lesson_id', 'update', 'partial_update', 'destroy', 'add_lesson_to_stu_course',
				'get_by_course_id', 'delete_lesson_from_stu_course'):
			permission_classes = (permissions.IsAdminUser | isInstructor, )
		else:
			permission_classes = [permissions.IsAdminUser]
		return [permission() for permission in permission_classes]
