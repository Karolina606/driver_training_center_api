from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})
    # password2 = serializers.CharField(style={'input_type': 'password'})
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pattern = re.compile(reg)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'groups', 'password']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'groups': {'required': False},
            'password': {'required': False, 'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        # validating conditions
        if re.search(self.pattern, attrs['password']):
            print("Password is valid.")
        else:
            raise serializers.ValidationError(
                {
                    "password": "Password must contain at least 8 signs, one small letter, one big letter, number and special sign."})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."})
        return attrs

    def create(self, validated_data):
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
        if 'admin' in self.validated_data['groups']:
            user.is_superuser = True
            user.is_staff = True
        user.save()
        return user

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            if attr == 'groups':
                instance.groups.add(value)
                if 'admin' in self.validated_data['groups']:
                    instance.is_superuser = True
                    instance.is_staff = True
            elif attr == 'permissions':
                instance.user_permissions.add(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance

    def save(self, *args, **kwargs):
        self.user = self.encrypt(self.user)
        super().save(*args, **kwargs)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', 'permissions']
        extra_kwargs = {
            'name': {'required': False},
            'permissions': {'required': False}
        }

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

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

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pattern = re.compile(reg)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        # validating conditions
        if re.search(self.pattern, attrs['password']):
            print("Password is valid.")
        else:
            raise serializers.ValidationError(
                {"password": "Password must contain at least 8 signs, one small letter, one big letter, number and special sign."})

        if User.objects.filter(email=attrs['username']).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
