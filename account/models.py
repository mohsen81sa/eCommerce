import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=64, null=True, blank=True) 
    
    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=256, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    



# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        try:
            user = User.objects.get(email_verification_token=value)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.email_verification_token = None
        instance.save()
        return instance

class ResendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value, is_active=False)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("No inactive user found with this email.")

# # views.py
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import EmailVerificationSerializer, ResendVerificationEmailSerializer
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.core.mail import send_mail
# from django.conf import settings
# import uuid

# User = get_user_model()

# class VerifyEmailAPIView(APIView):
#     serializer_class = EmailVerificationSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.validated_data['user']
#             serializer.update(user, serializer.validated_data)
#             return Response({"detail": "Email successfully verified."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ResendVerificationEmailAPIView(APIView):
#     serializer_class = ResendVerificationEmailSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.validated_data['user']
#             # Generate a new verification token
#             user.email_verification_token = uuid.uuid4()
#             user.save()

#             # Construct the verification URL
#             verification_url = request.build_absolute_uri(
#                 reverse('email-verify', kwargs={'token': str(user.email_verification_token)})
#             )

#             # Send the verification email (replace with your actual email sending logic)
#             send_mail(
#                 'Verify Your Email',
#                 f'Click the following link to verify your email: {verification_url}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],
#                 fail_silently=False,
#             )
#             return Response({"detail": "Verification email resent."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # urls.py
# from django.urls import path
# from .views import VerifyEmailAPIView, ResendVerificationEmailAPIView

# urlpatterns = [
#     path('email/verify/', VerifyEmailAPIView.as_view(), name='email-verify'),
#     path('email/resend/', ResendVerificationEmailAPIView.as_view(), name='email-resend'),
#     path('email/verify/<str:token>/', VerifyEmailAPIView.as_view(), name='email-verify-with-token'), # For link-based verification
# ]