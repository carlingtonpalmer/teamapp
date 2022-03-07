from rest_framework import serializers
from . import models



class QuoteSerializer(serializers.ModelSerializer):
    # doc = serializers.ListField(child=serializers.FileField(max_length=100,allow_empty_file=False, use_url=False))
    class Meta:
        model = models.Quote
        fields = ('userId','quote_type', 'chassis','cost', 'vehicle_use', 'claim_free_driving')
