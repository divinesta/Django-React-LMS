import random
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from api import serializers as api_serializers
from userauths.models import User, Profile


# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializers.RegisterSerializer



def generate_random_otp(length=7):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp

class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user = User.objects.filter(email=email).first()

        if user:
            
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            
            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()
            
            link = f'http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}'
            
            context = {
                "link": link,
                "username": user.username,
            }
            
            subject = "Password Reset Email"
            text_body = render_to_string('email/password_reset.txt', context)
            html_body = render_to_string('email/password_reset.html', context)
            
            message = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.email],
                body=text_body,
            )
            
            message.attach_alternative(html_body, "text/html")
            message.send()
            
            print("Link ===========", link)
        
        return user
    
class PasswordChangeAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_serializers.UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        payload = request.data
        
        otp = payload['otp']
        uuidb64 = payload['uuidb64']
        password = payload['password']
        
        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            # user.otp = ""
            user.save()
            
            return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)