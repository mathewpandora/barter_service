from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ad


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'user', 'title', 'description', 'image', 'category', 'condition', 'created_at', 'is_archived']
        read_only_fields = ['id', 'created_at', 'user']



