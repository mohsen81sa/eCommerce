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

from .serializers import PaymentSerializer

class PaymentView(drf_generics.GenericAPIView):
    serializer_class = PaymentSerializer
    
    def post(self, *args, **kwargs):
        serializer = PaymentSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data.get("amount")
        if amount < 0:
            return Response({"error": "Invalid amount. should be positive."}, status=400)
        elif amount < 10000:
            return Response({"error": "Invalid amount. should be higher than 10000"}, status=400)
        return Response({"detail": "Payment done."}, status=200)
