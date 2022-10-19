from django.contrib.auth.models import User
from django.db import models

class UserGroupChecker:
	@staticmethod
	def is_admin(user: User):
		return user.groups.filter(name='admin').exists()

	@staticmethod
	def is_instructor(user: User):
		return user.groups.filter(name='instructor').exists()

	@staticmethod
	def is_student(user: User):
		return user.groups.filter(name='student').exists()
