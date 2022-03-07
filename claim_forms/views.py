from django.shortcuts import render
from . import serializers, models
from rest_framework import views, generics
# Create your views here.



class ClaimFormView(generics.ListAPIView):
    serializer_class = serializers.ClaimFormSerializer
    queryset = models.ClaimsForm.objects.all()

