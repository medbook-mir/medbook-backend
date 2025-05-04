# myapp/serializers.py
from rest_framework import serializers
from .models import MedicalTest

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = ['id', 'name', 'age', 'created_at']