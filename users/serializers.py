from collections import Counter

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        c = Counter(email)
        if len(User.objects.filter(email=email).all()) == 1:
            raise serializers.ValidationError("User with this email already exist")
        if c['@'] != 1:
            raise serializers.ValidationError("Email should contain '@' sign")
        if not c['.']:
            raise serializers.ValidationError("Email is not valid")

        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError("The username should contain only alphanumeric character")
        return attrs

    def create(self, validated_data):
        return User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], username=validated_data['username'],
                                   password=make_password(validated_data['password']))


class CustomTokenObtainSerializer(serializers.Serializer):
    username_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(CustomTokenObtainSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        self.user = User.objects.filter(email=attrs[self.username_field]).first()

        if not self.user:
            raise ValidationError('User with such email does not exist.')

        if not self.user.check_password(attrs['password']):
            raise ValidationError('Incorrect credentials.')

        if self.user is None or not self.user.is_active:
            raise ValidationError('No active account found with the given credentials')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


