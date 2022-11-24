import datetime

from django.contrib.auth.models import User

from accounts.models import UserGroupChecker
from driver_training_center_db.models import Lesson, CourseStatus


def is_meeting_interfering(user: User, lessonToCheck: Lesson):
	if UserGroupChecker.is_student(user):
		statuses = CourseStatus.objects.filter(student_id=user.id)
		for status in statuses:
			lessons = Lesson.objects.filter(lesson_course_status=status)
			lessons2 = lessons.filter(start_date__gte=lessonToCheck.start_date, start_date__lte=lessonToCheck.end_date)
			lessons3 = lessons.filter(end_date__gte=lessonToCheck.start_date, end_date__lte=lessonToCheck.end_date)

			if len(lessons2) > 0 or len(lessons3) > 0:
				return True

			for lesson in lessons:
				min_date = datetime.datetime.min(lessonToCheck.start_date, lesson.start_date)
				max_date = datetime.datetime.max(lessonToCheck.end_date, lesson.end_date)
				if min_date == lesson.start_date and max_date == lesson.end_date:
					return True

		return False

	if UserGroupChecker.is_instructor(user):
		lessons = Lesson.objects.filter(instructor=user)
		lessons2 = lessons.filter(start_date__gte=lessonToCheck.start_date, start_date__lte=lessonToCheck.end_date)
		lessons3 = lessons.filter(end_date__gte=lessonToCheck.start_date, end_date__lte=lessonToCheck.end_date)

		if len(lessons2) > 0 or len(lessons3) > 0:
			return True

		# for lesson in lessons:
		# 	min_date = de.min(lessonToCheck.start_date, lesson.start_date)
		# 	max_date = datetime.datetime.max(lessonToCheck.end_date, lesson.end_date)
		# 	if min_date == lesson.start_date and max_date == lesson.end_date:
		# 		return True

		return False

