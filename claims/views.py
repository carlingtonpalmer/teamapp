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


# multiple upload working with email attachments
# class ClaimsView(views.APIView):
#     # serializer_class = serializers.ClaimSerializer
#     # queryset = models.Claim.objects.all()
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):

#         file_serializer = serializers.ClaimSerializer(data=request.data)

#         files = request.FILES.get('doc')#getlist('doc')
#         all_files = []

#         if file_serializer.is_valid():

#             claim_type = file_serializer.data['claim_type']
#             statement = file_serializer.data['statement']

#             user = request.user
#             body = 'Client has submitted a new claim.'
#             claim_info = "Claim: {}\nStatement: {}\n".format(claim_type,statement)
#             message = "Good day Admin, \n\n{} \n{} \nName: {} {}\nEmail:{}\nDOB:{}\nGender:{}\nPhone number:{}\nHome Address:{}\nLocation:{}\nEmployee #:{}\nTRN: {}\nEmployer: {}"#\nRegulation #:{}\nRank:{}
#             message_with_values = message.format(body, claim_info, user.first_name, user.last_name, user.email, user.dob, user.gender,user.phone_no,user.home_address, user.location, user.employee_number, user.trn, user.employer) #, user.regulation_number, user.rank,
                
#             email_from = settings.EMAIL_HOST_USER
#             to = [email_from, ]#to some admin user
#             try:
#                 email = EmailMessage('New Claim', message_with_values, email_from, to)

                
#                 # loop through list of uploaded files
#                 for f in request.FILES.getlist('doc'):
#                     all_files.append(f)

#                 # set the amount of files to count and attach multiple files to send
#                 count = len(all_files)
#                 for i in range(count):
#                     # print('i: {}'.format(i))
#                     email.attach(all_files[i].name, all_files[i].read(),all_files[i].content_type)#(files.name, files.read(),'image/png')
            
#                 # send email 
#                 email.send(fail_silently=False)
#                 # store info to db
#                 for f in request.FILES.getlist('doc'):
#                     models.Claim.objects.create(user=user, claim_type=claim_type, statement=statement, doc=f)
                    
#                 return response.Response(file_serializer.data, status=status.HTTP_201_CREATED)

#             except:
#                 return response.Response({'message': 'Either the attachment is too  big or corrupt'})
#         else:
#             # return response.Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return response.Response({'message': 'Unable to send email. Please try again later'})




class ClaimsView(views.APIView):
    # serializer_class = serializers.ClaimSerializer
    # queryset = models.Claim.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


    def send_email(self, request, context, files, user, file_serializer):

        claim_type = file_serializer.data['claim_type']
        statement = file_serializer.data['statement']

        print("first")
        all_files = []
        subject = 'New Claim Alert!!!'
        text_content = render_to_string('claims/email_template.txt', context, request=request)
        html_content = render_to_string('claims/email_template.html', context, request=request)

        from_email = settings.EMAIL_HOST_USER
        to = [from_email, ]#to some admin user teamappdev2019
        try:
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = 'html'

            # loop through list of uploaded files
            for f in request.FILES.getlist('doc'):
                all_files.append(f)

            # set the amount of files to count and attach multiple files to send
            count = len(all_files)
            for i in range(count):
                msg.attach(all_files[i].name, all_files[i].read(),all_files[i].content_type)#(files.name, files.read(),'image/png')
            
            # send email 
            msg.send(fail_silently=False)

            # store info to db
            for f in request.FILES.getlist('doc'):
                models.Claim.objects.create(user=user, claim_type=claim_type, statement=statement, doc=f)

        except:
            return response.Response({'message': 'Either the attachment is too  big or corrupt'}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, *args, **kwargs):

        file_serializer = serializers.ClaimSerializer(data=request.data)

        files = request.FILES.get('doc')#getlist('doc')

        if file_serializer.is_valid():

            claim_type = file_serializer.data['claim_type']
            statement = file_serializer.data['statement']

            user = request.user
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
              'claim_type': claim_type,
              'statement': statement,
            })

            self.send_email(request, context, files, user, file_serializer)
                    
            return response.Response(file_serializer.data, status=status.HTTP_201_CREATED)

        else:
            # return response.Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return response.Response({'message': 'Unable to send email. Please try again later'}, status=status.HTTP_400_BAD_REQUEST)

