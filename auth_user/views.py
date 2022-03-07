from rest_framework import generics, viewsets
from . import serializers as custom_serializer
from users import models, serializers
from django.contrib.auth import get_user_model
# Create your views here.


class AuthListView(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = custom_serializer.AuthUserSerializer
    
