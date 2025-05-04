import uuid

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.core.mail import send_mail

from rest_framework import generics as drf_generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions as drf_perms
from rest_framework.authtoken.models import Token

from .models import *
from .serializers import *

class RegistrationView(TemplateView):
    template_name = "register.html"
    
    def get_context_data(self, **kwargs):
        return {}


class SendEmailVerificationView(drf_generics.GenericAPIView):
    serializer_class = SendEmailVerificationSerializer
    permission_classes = [drf_perms.AllowAny]
    
    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        
        email_verification, created = EmailVerification.objects.get_or_create(email=email)
        if not created:
            email_verification.token = uuid.uuid4()
            email_verification.created_at = timezone.now()
            
        # send_mail(
        #     'Verify Your Email',
        #     f'Click the following link to verify your email: {verification_url}',
        #     settings.DEFAULT_FROM_EMAIL,
        #     [email],
        #     fail_silently=False,
        # )
        
        return Response({"detail": "Email sent successfully."}, status=200)
        

class SignupView(drf_generics.GenericAPIView):
    serializer_class = SignupSerializer
    permission_classes = [drf_perms.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        
        user = get_user_model().objects.create(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        
        login(request=request, user=user)
        
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"key": token.key,}, status=status.HTTP_201_CREATED)
        
        
class LoginView(drf_generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [drf_perms.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        print(username, password)
        
        user = get_user_model().objects.filter(username=username).first()
        
        
        if not user:
            return Response({"error": "Please first register."}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.check_password(password):
            login(request=request, user=user)        
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"key": token.key,}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class GetUserProfileView(drf_generics.GenericAPIView):
    permission_classes = [drf_perms.IsAuthenticated]
    
    def get(self, *args, **kwargs):
        return Response(data={"username": self.request.user.username})