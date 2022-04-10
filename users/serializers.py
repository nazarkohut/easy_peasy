from django.contrib.auth.models import User
from django.core.validators import validate_email
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from misc.validators import simple_email_validation


class UserSerializer(UserCreateSerializer):
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(max_length=64)
    last_name = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        simple_email_validation(email)
        validate_email(email)
        if len(User.objects.filter(email=email).all()) >= 1:
            raise serializers.ValidationError("User with this email already exist")

        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError("The username should contain only alphanumeric character")
        return attrs


class EmailTokenObtainSerializer(serializers.Serializer):
    username_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(min_length=6)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs[self.username_field]).first()

        if not user:
            raise ValidationError('User with such email does not exist.')

        if not user.check_password(attrs['password']):
            raise ValidationError('Incorrect credentials.')

        if user is None or not user.is_active:
            raise ValidationError('No active account found with the given credentials')

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')


class EmailTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        email = attrs['email']
        simple_email_validation(email)
        validate_email(email)
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError("User with given email does not exist.")
        data = super().validate(attrs)

        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class CustomTokenObtainSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = PasswordField(min_length=6)


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)


class UsernameTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    def validate(self, attrs):
        user = User.objects.filter(username=attrs['username']).first()

        if not user:
            raise serializers.ValidationError("User with given username does not exist.")

        data = super().validate(attrs)
        refresh = self.get_token(user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class BlackListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlacklistedToken
        fields = ('refresh', )

    def validate(self, attrs):
        if 'refresh' not in attrs:
            raise ValidationError({"refresh": ["This field is required"]})
        if not attrs['refresh']:
            raise ValidationError({"refresh": ["May not be blank"]})
        return attrs
