from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import UserGroupChecker
from accounts.serializers import UserSerializer, GroupSerializer, PermissionSerializer, MyTokenObtainPairSerializer, \
	RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

	def get_queryset(self):
		user = self.request.user
		queryset = None
		if user.is_superuser or UserGroupChecker.is_admin(user):
			queryset = User.objects.all()
		elif UserGroupChecker.is_instructor(user) or UserGroupChecker.is_student(user):
			queryset = User.objects.filter(id=user.id)
		return queryset

	@action(detail=True, methods=['post'])
	def grand_admin(self, request, pk=None):
		user = User.objects.get(id=pk)
		user.groups.add(Group.objects.get(name='admin'))
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return Response()

	@action(detail=True, methods=['post'])
	def grand_instructor(self, request, pk=None):
		user = User.objects.get(id=pk)
		user.groups.add(Group.objects.get(name='instructor'))
		user.save()
		return Response()

	@action(detail=True, methods=['post'])
	def grand_student(self, request, pk=None):
		user = User.objects.get(id=pk)
		user.groups.add(Group.objects.get(name='student'))
		user.save()
		return Response()

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""
		permission_classes = []
		if self.action in ('list', 'retrieve', 'update', 'partial_update', 'destroy'):
			permission_classes = [permissions.IsAuthenticated]
		elif self.action == 'grand_admin':
			permission_classes = [permissions.IsAdminUser]
		else:
			pass
		return [permission() for permission in permission_classes]


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


class MyTokenObtainPairView(TokenObtainPairView):
	serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	permission_classes = (AllowAny,)
	serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
	routes = [
		'/accounts/token/',
		'/accounts/register/',
		'/accounts/token/refresh/'
	]
	return Response(routes)

