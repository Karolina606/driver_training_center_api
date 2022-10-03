from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
	name = models.CharField(max_length=200, null=False)
	users = models.ManyToManyField(User, related_name="user_role")

	class Meta:
		db_table = "role"


class Permission(models.Model):
	name = models.CharField(max_length=200, null=False)
	roles = models.ManyToManyField(Role, related_name="role_permission")

	class Meta:
		db_table = "permission"


class DrivingLicenseCategory(models.Model):
	name = models.CharField(max_length=200, null=False)
	theory_full_time = models.DecimalField(max_digits="100", decimal_places="0", null=False)
	practice_full_time = models.DecimalField(max_digits="100", decimal_places="0", null=False)

	class Meta:
		db_table = "driving_license_category"


class Course(models.Model):
	driving_license_category = models.ForeignKey(
		DrivingLicenseCategory,
		related_name="courses",
		on_delete=models.CASCADE,
		null=False)
	start_date = models.DateTimeField(null=False)

	class Meta:
		db_table = "course"


class LessonType(models.TextChoices):
	THEORY_LECTURE = 'T', 'theory'
	PRACTICAL_LESSON = 'P', 'practice'


class Lesson(models.Model):
	instructor = models.ForeignKey(User, related_name="instructor_lessons", on_delete=models.CASCADE, null=False)
	course = models.ForeignKey(Course, related_name="course_lessons", on_delete=models.CASCADE, null=False)
	type = models.CharField(choices=LessonType.choices, max_length=20, null=False)
	start_date = models.DateTimeField(null=False)
	end_date = models.DateTimeField(null=False)

	class Meta:
		db_table = "lesson"


class StudentCourseStatus(models.Model):
	student = models.ForeignKey(User, related_name="student_course_status", on_delete=models.CASCADE, null=False)
	course = models.ForeignKey(User, related_name="course_status_for_student", on_delete=models.CASCADE, null=False)
	paid_money = models.DecimalField(max_digits=6, decimal_places=2, null=False)
	is_course_paid = models.BooleanField(default=False, null=False)
	is_internal_theoretical_exam_passed = models.BooleanField(default=False, null=False)
	is_internal_practical_exam_passed = models.BooleanField(default=False, null=False)
	lessons = models.ManyToManyField(Lesson, related_name="lesson_student_course_status")

	class Meta:
		db_table = "student_course_status"
