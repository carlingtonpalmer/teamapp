from rest_framework import serializers
from users import models

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.http import HttpResponse


class TestSerializer(serializers.Serializer):
    # serilaize a field for testing POST, UPDATE, PUT
    fname = serializers.CharField(max_length=15)
    lname = serializers.CharField(max_length=10)


class UserSerializer(serializers.ModelSerializer):
    """ use to serialze a user model or object"""
    #when using modelserializer you use meta class to configure the serializer to point to a specific model

    class Meta:
        model = models.User
        fields = ['id','first_name', 'last_name', 'email',  'password', 'phone_no', 'gender', 'dob', 'home_address', 'location', 'employee_number', 'regulation_number', 'rank', 'trn', 'employer']

        extra_kwargs = {
            'password' : {
                'write_only': True,
                'style' : {'input_type' : 'password'}
                }
        }

    
#    def create(self, validated_data):
#        """ override this create default user function to use the custom create_user method from user manager.
#        One of the reason for this to ensure that password is hash etc """
#
#        user = models.User.objects.create_user(
#            validated_data['first_name'],
#            validated_data['last_name'],
#            validated_data['email'],
#            password = validated_data['password']
#        )
#
#        return user


    def create(self, validated_data):
        """ override this create default user function to use the custom create_user method from user manager.
        One of the reason for this to ensure that password is hash etc """

        user = models.User.objects.create_user(
            validated_data['first_name'],
            validated_data['last_name'],
            validated_data['email'],
            password = validated_data['password']
        )
        user = models.User.objects.filter(pk=user.id).first()
        
        self.email(user, 'New user', 'You have a new registered user.')
        return user

    def email(self, user, subject_text, body):
        print('Test')
        print(user.dob)

        print('email test')
        subject = subject_text

        message = "Good day Admin, \n\n{}: \nName: {} {}\nEmail:{}\nDOB:{}\nGender:{}\nPhone number:{}\nHome Address:{}\nLocation:{}\nEmployee #:{}\nRegulation #:{}\nRank:{}\nTRN: {}\nEmployer: {}"
        message_with_values = message.format(body, user.first_name, user.last_name, user.email, user.dob, user.gender,user.phone_no,user.home_address, user.location, user.employee_number, user.regulation_number, user.rank, user.trn, user.employer)
        
        print('message')
        print(message_with_values)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['teamappdev2019@gmail.com',]
        # send_mail( subject, message, email_from, recipient_list )
        email = EmailMessage(subject, message_with_values, email_from, recipient_list)
        # email.attach_file(''+photo)
        email.send()



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id','first_name', 'last_name', 'email','phone_no', 'gender', 'dob', 'home_address', 'location', 'employee_number', 'regulation_number', 'rank', 'trn', 'employer']

        read_only_fields = ['id','first_name', 'last_name', 'email']
        
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)

         # return the user model
        user = models.User.objects.filter(pk=user.id).first()

        # send email function call accepting 2 objects
#        userSerializerObj = UserSerializer()
#        userSerializerObj.email(user,'User profile update', 'An update was made from client')
        return user

#original
#class ProductSubCatergorySerializer(serializers.ModelSerializer):
#
#    prod = serializers.CharField(source='prod_id.id', read_only=True)
#    class Meta:
#        model = models.ProductSubCategory
#        fields = ('id','title', 'body','prod')

class ProductSubCatergorySerializer(serializers.ModelSerializer):

    cat_title = serializers.CharField(source='prod_id.title', read_only=True)
    cat_id = serializers.CharField(source='prod_id.id', read_only=True)
    cat_slug= serializers.CharField(source='prod_id.slug', read_only=True)
    class Meta:
        model = models.ProductSubCategory
        fields = ('id','title', 'body','cat_id', 'cat_title', 'is_interested', 'cat_slug')
        read_only_fields = ['id','title', 'body', 'cat_title', 'cat_id','cat_slug']


class ProductCategorySerializer(serializers.ModelSerializer):
    #   list = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = models.ProductCategory
        fields = ('id', 'title','icon','slug') # new changes 14/02/202
        look_up = ('slug', 'prod_id')
        extra_kwargs = {
            'url' : {'lookup_field': 'slug'}
        }


class ConfirmEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfirmEmailNew
        fields = ('user',)

class ConfirmEmailCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConfirmEmailNew
        fields = ('user','code')