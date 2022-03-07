from rest_framework import serializers
from . import models



class ClaimSerializer(serializers.ModelSerializer):
    doc = serializers.ListField(child=serializers.FileField(max_length=100,allow_empty_file=False, use_url=False))
    class Meta:
        model = models.Claim
        fields = ('user','claim_type', 'statement','doc')


# class ClaimSerializer2(serializers.ModelSerializer):
#     # doc = serializers.ListField(child=serializers.FileField(max_length=100,allow_empty_file=False, use_url=False))
#     class Meta:
#         model = models.Claim
#         fields = ('user','title', 'statement','doc')

# class ClaimSerializer3(serializers.ModelSerializer):
#     doc = serializers.ListField(child=serializers.FileField(max_length=100,allow_empty_file=False, use_url=False))
#     class Meta:
#         model = models.Claim
#         fields = ('user','title', 'statement','doc')


# class DocumentSerializer(serializers.ModelSerializer):
#     doc = serializers.ListField(child=serializers.FileField(max_length=100,allow_empty_file=False, use_url=False))
#     class Meta:
#         model = models.Document
#         fields = ('doc',)