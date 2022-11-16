from django.contrib.auth.models import User
from django.db import models
from rest_framework import permissions


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


class isInstructor(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(request.user.groups.filter(name='instructor').exists())


class isStudent(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.user.groups.filter(name='student').exists()
