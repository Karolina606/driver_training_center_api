from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import UserGroupChecker, isInstructor
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

	@action(detail=True, methods=['post'], name='grand_admin')
	def grand_admin(self, request, pk=None):
		user = User.objects.get(id=pk)
		user.groups.add(Group.objects.get(name='admin'))
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return Response()

	@action(detail=True, methods=['post'], name='grand_instructor')
	def grand_instructor(self, request, pk=None):
		user = User.objects.get(id=pk)
		user.groups.add(Group.objects.get(name='instructor'))
		user.save()
		return Response()

	@action(detail=True, methods=['post'], name='grand_student')
	def grand_student(self, request, pk=None):
		user = User.objects.get(id=pk)
		user.groups.add(Group.objects.get(name='student'))
		user.save()
		return Response()

	@action(detail=False, methods=['get'], name='instructors')
	def instructors(self, request):
		if UserGroupChecker.is_instructor(request.user):
			print(request.user)
			users = User.objects.filter(username=request.user).values()
		else:
			users = User.objects.filter(groups=Group.objects.get(name='instructor')).values()
		return Response(users)

	@action(detail=False, methods=['get'], name='students')
	def students(self, request):
		users = User.objects.filter(groups=Group.objects.get(name='student')).values()
		return Response(users)

	@action(detail=False, methods=['get'], name='admins')
	def admins(self, request):
		users = User.objects.filter(groups=Group.objects.get(name='admin')).values()
		return Response(users)

	@action(detail=True, methods=['get'], name='name_of_user')
	def name_of_user(self, request, pk=None):
		user = User.objects.get(id=pk)
		username = user.username
		first_name = user.first_name
		last_name = user.last_name
		return Response({'username': username, 'first_name': first_name, 'last_name': last_name})

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""

		permission_classes = []
		if self.action in ('list', 'retrieve'):
			permission_classes = [permissions.IsAuthenticated]
		elif self.action in ('retrieve', 'update', 'partial_update', 'destroy', 'name_of_user'):
			permission_classes = (permissions.IsAdminUser | isInstructor,)
		elif self.action in ('grand_admin', 'grand_instructor', 'grand_student'):
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

	def get_permissions(self):
		"""
		Instantiates and returns the list of permissions that this view requires.
		"""

		permission_classes = []
		if self.action in ('list', 'retrieve'):
			permission_classes = [permissions.IsAuthenticated]
		else:
			permission_classes = [permissions.IsAdminUser]
		return [permission() for permission in permission_classes]


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
