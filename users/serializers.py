from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if len(User.objects.filter(email=email).all()) == 1:
            raise serializers.ValidationError("User with this email already exist")

        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError("The username should contain only alphanumeric character")
        return attrs

        # here will be email validation

    def create(self, validated_data):
        return User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], username=validated_data['username'],
                                   password=make_password(validated_data['password']))



