from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import labUser

class LabUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = labUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'state']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role

        return token
