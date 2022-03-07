from django.shortcuts import render
from rest_framework import views,generics
from rest_framework import response, status
from rest_framework.parsers import MultiPartParser, FormParser
from . import models, serializers
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.auth.models import Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
import os
import mimetypes

# Create your views here.

class QuoteView(views.APIView):


    def send_email(self, request, context, user):

        print("first")
        subject = 'New Quote!!!'
        text_content = render_to_string('quotes/email_template.txt', context, request=request)
        html_content = render_to_string('quotes/email_template.html', context, request=request)

        from_email = settings.EMAIL_HOST_USER
        to = [from_email, ]#to some admin user 
        try:
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = 'html'

            # send email 
            msg.send(fail_silently=False)

            # store info to db
            models.Quote.objects.create(userId=user, quote_type=quote_type, chassis=chassis, cost=cost, vehicle_use=vehicle_use, claim_free_driving=claim_free_driving)

        except:
            return response.Response({'message': 'Unable to process email at this time.'}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, *args, **kwargs):

        quote_serializer = serializers.QuoteSerializer(data=request.data)


        if quote_serializer.is_valid():

            user = request.user
            quote_type = quote_serializer.data['quote_type']
            chassis = quote_serializer.data['chassis']
            cost = quote_serializer.data['cost']
            vehicle_use = quote_serializer.data['vehicle_use']
            claim_free_driving = quote_serializer.data['claim_free_driving']

            context = ({
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'phone_no': user.phone_no,
            'gender': user.gender,
            'dob': user.dob,
            'home_address': user.home_address,
            'location': user.location,
            'employee_number': user.employee_number,
            'trn': user.trn,
            'employer': user.employer,
            'quote_type': quote_type,
            'chassis': chassis,
            'cost': cost,
            'vehicle_use': vehicle_use,
            'claim_free_driving': claim_free_driving,
        })


            # email function
            self.send_email(request, context, user)

            return response.Response(quote_serializer.data, status=status.HTTP_201_CREATED)
        else:

            return response.Response({"message" : "Unable to request quotes. Try again later."}, status=status.HTTP_400_BAD_REQUEST)
       
