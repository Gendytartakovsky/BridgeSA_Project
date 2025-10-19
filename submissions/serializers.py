from rest_framework import serializers
from .models import DocumentSubmission
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class DocumentSubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DocumentSubmission
        fields = ['id', 'title', 'description', 'document', 'submitted_at', 'status', 'reference_code', 'user']
        read_only_fields = ['submitted_at', 'status', 'reference_code']
