from rest_framework import serializers
from users.models import User
# from django.contrib.auth import get_user_model
# from rest_auth.serializers import LoginSerializer
class AuthUserSerializer(serializers.ModelSerializer):

    class Meta: 
        model = User
        fields = ['id','first_name', 'last_name', 'email',  'password']
        # read_only_fields = ('email',)
        extra_kwargs = {
            'password' : {
                'write_only': True,
                'style' : {'input_type' : 'password'}
                }
        }

    
    def create(self, validated_data):
        """ override this create default user function to use the custom create_user method from user manager. 
        One of the reason for this to ensure that password is hash etc """
        user = User.objects.create_user(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password']            
        )

        return user

