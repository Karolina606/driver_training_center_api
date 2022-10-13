from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'groups', 'password']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'groups': {'required': False},
            'password': {'required': False, 'write_only': True}
        }

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        user.groups.set(self.validated_data['groups'])
        user.user_permissions.set(self.validated_data['permissions'])
        user.save()
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'permissions']

    def save(self):
        group = Group(name=self.validated_data['name'])
        group.save()
        group.permissions.set(self.validated_data['permissions'])
        group.save()
        return group


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['url', 'name']
