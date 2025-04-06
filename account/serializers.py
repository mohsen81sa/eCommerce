from rest_framework import serializers
from django.contrib.auth import get_user_model


class SignupSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField()
    
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password", "password_confirmation") 
        
    def validate_password_confirmation(self, data):
        if data != self.initial_data["password"]:
            raise serializers.ValidationError("password and password_confirmation mismatch.")


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "password")