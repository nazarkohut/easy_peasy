from django.contrib.auth.models import User
from django.core.validators import validate_email
from djoser.serializers import UserCreateSerializer, SendEmailResetSerializer, PasswordSerializer, \
    CurrentPasswordSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import PasswordField, TokenObtainSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from misc.validators import simple_email_validation, isalnum_validator


class UserSerializer(UserCreateSerializer):
    email = serializers.CharField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=128, validators=[isalnum_validator])
    first_name = serializers.CharField(required=True, max_length=64, validators=[isalnum_validator])
    last_name = serializers.CharField(required=True, max_length=64, validators=[isalnum_validator])
    password = serializers.CharField(required=True, max_length=64, min_length=6, write_only=True)

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
        if len(User.objects.filter(username=username).all()) >= 1:
            raise serializers.ValidationError("User with this username already exist")
        return attrs


class EmailTokenObtainSerializer(serializers.Serializer):
    username_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(max_length=254)
        self.fields['password'] = PasswordField(min_length=6)

    def validate(self, attrs):
        email = attrs[self.username_field]
        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User with given email does not exist.")
        if not user.check_password(attrs['password']):
            raise ValidationError({'detail': ['This credentials did not work. Please, try again.']})

        if user is None or not user.is_active:
            raise ValidationError({'detail': ['No active account found with the given credentials. '
                                              'Note: please, make sure you activated your account.']})

        return user

    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')


class EmailTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return CustomRefreshToken.custom_for_user(user)

    def validate(self, attrs):
        email = attrs['email']
        simple_email_validation(email)
        validate_email(email)
        user = super().validate(attrs)

        refresh = self.get_token(user)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class CustomTokenObtainSerializer(TokenObtainSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField(max_length=128, validators=[isalnum_validator])
        self.fields['password'] = PasswordField(min_length=6)

    def validate(self, attrs):
        username = attrs[self.username_field]

        user = User.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError("User with given username does not exist.")

        if not user.check_password(attrs['password']):
            raise ValidationError({'detail': ['This credentials did not work. Please, try again.']})

        if user is None or not user.is_active:
            raise ValidationError({'detail': ['No active account found with the given credentials. '
                                              'Note: please, make sure you activated your account.']})
        return user


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        token = CustomRefreshToken.custom_for_user(user)
        return token


class CustomRefreshToken(RefreshToken):
    @classmethod
    def custom_for_user(cls, user):
        token = cls.for_user(user)
        token['full_name'] = user.first_name + " " + user.last_name
        token['username'] = user.username
        return token


class UsernameTokenObtainPairSerializer(CustomTokenObtainPairSerializer):
    def validate(self, attrs):
        user = super().validate(attrs)
        refresh = self.get_token(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class BlackListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlacklistedToken
        fields = ('refresh',)

    def validate(self, attrs):
        if 'refresh' not in attrs:
            raise ValidationError({"refresh": ["This field is required"]})
        if not attrs['refresh']:
            raise ValidationError({"refresh": ["May not be blank"]})
        return attrs


class CustomSendEmailResetSerializer(SendEmailResetSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.email_field] = serializers.EmailField(max_length=254)


class ResetPasswordSendEmailSerializer(CustomSendEmailResetSerializer):
    def validate(self, attrs):
        email = attrs.get('email', '')
        user = User.objects.filter(email=email).first()
        if not user or not user.is_active:
            raise serializers.ValidationError(self.default_error_messages['email_not_found'])
        return attrs


class CustomResendActivationEmailSerializer(CustomSendEmailResetSerializer):
    def validate(self, attrs):
        email = attrs.get('email', '')
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(self.default_error_messages['email_not_found'])
        if user.is_active:
            raise serializers.ValidationError("User with this email already activated.")
        return attrs


# Set new password serializers
class CustomPasswordSerializer(PasswordSerializer):
    new_password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, attrs):
        return super().validate(attrs)


class CustomCurrentPasswordSerializer(CurrentPasswordSerializer):
    current_password = serializers.CharField(max_length=64)


class CustomSetPasswordSerializer(CustomPasswordSerializer, CustomCurrentPasswordSerializer):
    pass
