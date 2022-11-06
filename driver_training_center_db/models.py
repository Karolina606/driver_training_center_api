from django.contrib.auth.models import User
from django.db import models


class DrivingLicenseCategory(models.Model):
	name = models.CharField(max_length=200, null=False)
	theory_full_time = models.DecimalField(max_digits=100, decimal_places=0, null=False)
	practice_full_time = models.DecimalField(max_digits=100, decimal_places=0, null=False)

	class Meta:
		db_table = "driving_license_category"

	def __str__(self):
		return f'Category: {self.name}, theory full time: {self.theory_full_time}, ' \
				f'practice full time: {self.practice_full_time}'


class Course(models.Model):
	driving_license_category = models.ForeignKey(
		DrivingLicenseCategory,
		related_name="courses",
		on_delete=models.CASCADE,
		null=False)
	start_date = models.DateTimeField(null=False)

	class Meta:
		db_table = "course"

	def __str__(self):
		return f'Kategoria: {self.driving_license_category.name}, start: {self.start_date.ctime()}'


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

	def __str__(self):
		return f'Course: {self.course_id}, type: {self.type}, instructor: {self.instructor.first_name}' \
				f' {self.instructor.last_name}, start: {self.start_date.ctime()}, end: {self.end_date.ctime()}'


class CourseStatus(models.Model):
	student = models.ForeignKey(User, related_name="student_course_status", on_delete=models.CASCADE, null=False)
	course = models.ForeignKey(Course, related_name="course_status_for_student", on_delete=models.CASCADE, null=False)
	paid_money = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	is_course_paid = models.BooleanField(default=False, null=True)
	is_internal_theoretical_exam_passed = models.BooleanField(default=False, null=True)
	is_internal_practical_exam_passed = models.BooleanField(default=False, null=True)
	lessons = models.ManyToManyField(Lesson, related_name="lesson_course_status", null=True)

	class Meta:
		db_table = "course_status"
