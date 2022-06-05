from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

def get_and_authenticate_user(email, password):
    user = authenticate(username=email, password=password)
    if user is not None:
            # A backend authenticated the credentials
            return user
    else:
        # No backend authenticated the credentials
        raise serializers.ValidationError("Invalid username/password. Please try again!")
    

def create_user_account(username,email, password, 
                        **extra_fields):
    
    user = get_user_model().objects.create_user(username=username,
                        email=email, password=password, **extra_fields)
    return user