from rest_framework import serializers
from . import models


class ClaimFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClaimsForm
        fields = '__all__'

