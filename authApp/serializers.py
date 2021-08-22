from rest_framework import serializers
from .models import labUser

class LabUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = labUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'state']