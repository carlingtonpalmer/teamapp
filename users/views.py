from rest_framework import response
from rest_framework import status #, viewsets
from users import serializers, models, permissions
from rest_framework import viewsets, filters,generics, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from random import randint
import json

# Create your views here.

class UserViewset(generics.ListAPIView):
    """ this class is use for creating and updating users """

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all() # just tell django we gonna use CREATE, UPDATE, RETRIEVE LIST ETC.
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.ModifyOwnProfile,)
    permission_classes = [IsAuthenticated]
    # filter_backends = (filters.SearchFilter, )
    # search_fields = ('email', 'first_name', 'last_name',)
    # token, created = Token.objects.get_or_create(user=user)
    # response.Response({"token": token.key})
    




class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.User.objects.all()
    permission_classes = (permissions.ModifyOwnProfile,)



# class ProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Profile.objects.all()
#     serializer_class = serializers.UserProfileSerializer

# class ProfileCreateView(generics.ListCreateAPIView):
#     queryset = models.Profile.objects.all()
#     serializer_class = serializers.UserProfileSerializer



    
class LoginUserApiView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({
              'id': user.id,
              'first_name': user.first_name,
              'last_name' : user.last_name,
              'email' : user.email,
              'token': token.key,
              'phone_no': user.phone_no,
              'gender': user.gender,
              'dob': user.dob,
              'home_address': user.home_address,
              'location': user.location,
              'employee_number': user.employee_number,
            #   'regulation_number': user.regulation_number,
            #   'rank': user.rank,
              'trn': user.trn,
              'employer': user.employer,
        })

class LogoutUserView(views.APIView):

    permission_classes = [AllowAny]

    def post(self, request,*args, **kwargs):
        logout(request)
        return response.Response(
            {
                "message" : "User was logged out successfully."
            },
            status=status.HTTP_200_OK

        )

# working pass word not hashing and saving
# @api_view(['POST', 'GET'])
class CreateUserView(ObtainAuthToken, generics.ListCreateAPIView):

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all() # just tell django we gonna use CREATE, UPDATE, RETRIEVE LIST ETC.
    # # authentication_classes = (TokenAuthentication,)
    # # permission_classes = (permissions.ModifyOwnProfile,)
    # # filter_backends = (filters.SearchFilter, )
    # # search_fields = ('email', 'first_name', 'last_name',)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = serializers.UserSerializer(data=request.data)
            # serializer = self.serializer_class(data=request.data, context={'request': request})
            
            if serializer.is_valid():

                # id = serializer.data.get('id')
                fn = serializer.data.get('first_name')
                ln = serializer.data.get('last_name')
                email = serializer.data.get('email')
                password = serializer.data.get('password')
                user = models.User.objects.create_user(fn,ln,email)
                user.set_password(password)
                user.save()
                # user = serializer.validated_data['user']
                # serializer.save()
                # print('User test: {}'.format(user.email))
                token = Token.objects.create(user=user)
                print('User Test: {}'.format(email))
                print('Token Test: {}'.format(token.key))
                print('ID Test: {}'.format(user.id))
                print('Pass Test: {}'.format(user.password))
                return response.Response(
                    {
                    'id': user.id,#serializer.data.get('id'),
                    'first_name': user.first_name,#serializer.data.get('first_name'),
                    'last_name' : user.last_name,#serializer.data.get('last_name'),
                    'email' : user.email,#serializer.data.get('email'),
                    'token': token.key,
                },
                status=status.HTTP_201_CREATED
                )
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# works perfect using register view
class Register(views.APIView):

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = serializers.UserSerializer(data=request.data)
            # serializer = self.serializer_class(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                user = serializer.save()
                token = Token.objects.create(user=user)
                print('User Test: {}'.format(user.email))
                print('Token Test: {}'.format(token.key))
                print('ID Test: {}'.format(user.id))
                print('Pass Test: {}'.format(user.password))
                return response.Response(
                    {
                    'id': user.id,#serializer.data.get('id'),
                    'first_name': user.first_name,#serializer.data.get('first_name'),
                    'last_name' : user.last_name,#serializer.data.get('last_name'),
                    'email' : user.email,#serializer.data.get('email'),
                    'token': token.key,
                    'phone_no': user.phone_no,
                    'gender': user.gender,
                    'dob': user.dob,
                    'home_address': user.home_address,
                    'location': user.location,
                    'employee_number': user.employee_number,
                    # 'regulation_number': user.regulation_number,
                    # 'rank': user.rank,
                    'trn': user.trn,
                    'employer': user.employer,
                },
                status=status.HTTP_201_CREATED
                )
            return response.Response({'message': 'Unable to register user.'},status=status.HTTP_400_BAD_REQUEST)
            
            


class ProductCategoryView(generics.ListAPIView): # new changes 14/02/202
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    
    
class ProductSubCategoryDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSubCatergorySerializer
    queryset = models.ProductSubCategory.objects.all()



class ProductSubCategoryListSlugView(generics.ListAPIView):
    serializer_class = serializers.ProductSubCatergorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.ProductSubCategory.objects.all()
    
        slug = self.kwargs.get('slug', None)
        # print('Slug: {}'.format(slug))
        
        queryset = queryset.filter(prod_id_id__slug=slug)
        # queryset = models.ProductSubCategory.objects.filter(slug=slug)#.values_list()

        return queryset



class SingleProductView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSubCatergorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.ProductSubCategory.objects.all()
  
        id = self.kwargs.get('pk', None) #getting values from browser
        slug = self.kwargs.get('slug', None)
        # print('ID: {}'.format(id))

        queryset = queryset.filter(prod_id_id__slug=slug).order_by('id')
        # for q in queryset:

        # print('title: {}'.format(queryset[id]))
        # self.send_email1(self,request)
        return queryset

    def send_email(self, request, context, user):

        subject = 'Product Alert!!!'
        text_content = render_to_string('users/email_template.txt', context, request=request)
        html_content = render_to_string('users/email_product_template.html', context, request=request)

        from_email = settings.EMAIL_HOST_USER
        print('Email: {}'.format(from_email))
        to = [from_email, ]#to some admin user
        try:
           print("email try")
           msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
           msg.attach_alternative(html_content, "text/html")
           msg.content_subtype = 'html'

           # send email
           msg.send(fail_silently=False)

        except:
           return response.Response({'message': 'Unable to send email.'}, status=status.HTTP_502_BAD_GATEWAY)
           # return response.Response({'message': 'Either the attachment is too  big or corrupt'})





    def post(self, request, *args, **kwargs):

        id = self.kwargs.get('pk', None) #getting values from browser
        # slug = self.kwargs.get('slug', None)

        # queryset = models.ProductSubCategory.objects.only('prod_id_id').get(prod_id_id=2).prod_id_id
        # # queryset = queryset.filter(prod_id_id=2).order_by('id')
        # print('Test: {}'.format(queryset))

        # solution url: http://morozov.ca/tip-how-to-get-a-single-objects-value-with-django-orm.html
        prod_title = models.ProductSubCategory.objects.only('title').get(id=id).title #

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
            'prod_title': prod_title,
        })
        try:
            #send email function
            self.send_email(request, context, user)

            return response.Response({'message': 'email was sent'})
        except:
            # return response.Response({'message': 'Oops something went wrong!!!'})
            return response.Response({'message': 'Unable to signup user for product.'}, status=status.HTTP_406_NOT_ACCEPTABLE)



class SendEmail():

    def send_email(self, request, context, user, subject, template_name):

        print("email top")
        subject = subject
        print('Context1: {}'.format(context))
        text_content = render_to_string(template_name+'.txt', context, request=request)
        print("email middle test")
        html_content = render_to_string(template_name+'.html', context, request=request)

        print("email middle: ")
        from_email = settings.EMAIL_HOST_USER
        print('Email: {}'.format(from_email))
        print('Email address: {}'.format(user))
        to = [user, ]#to some admin user
        try:
            print("email try")
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.content_subtype = 'html'

            # send email 
            msg.send(fail_silently=False)

        except:
            # return response.Response({'message': 'Unable to send email at this time please try again later.'})
            return response.Response({'message': 'Unable to send email at this time please try again later.'}, status=status.HTTP_502_BAD_GATEWAY)



class ConfirmEmailView(views.APIView):
    serializer_class = serializers.ConfirmEmailSerializer
    permission_classes = [AllowAny]

    def generater(self):
        """ generate random code verification code """
        list_no = []
        for rand in range(6):
            random_no = randint(0,6)
            list_no.append(random_no)
            print("Random: {}".format(rand))
        
        print("Random List: {}".format(list_no))

        return list_no

    
    def post(self, request, *args, **kwargs):
        serializer_class = serializers.ConfirmEmailSerializer(data=request.data,)
        code_serializer = serializers.ConfirmEmailCodeSerializer
        queryset = models.ConfirmEmailNew.objects.all()
        user_queryset = models.User.objects.all()


        # user = request.user
        if serializer_class.is_valid():
            user = serializer_class.data.get('user')


            code = self.generater()
            string = ''.join(map(str, code)) 
            print(code_serializer)
            context = {
                'user': user,
                "string": string 
            }

            if not queryset.filter(user=user).exists() and not user_queryset.filter(email=user):
                models.ConfirmEmailNew.objects.create(user=user, code=string)
                send_mail = SendEmail()
                send_mail.send_email(request, context, user, 'Verify user account.','users/email_confirm_template')

            elif user_queryset.filter(email=user):
                return response.Response({"message": "User already a registered."}, status=status.HTTP_403_FORBIDDEN)

            else:

                return response.Response({'message': 'Code was already sent to user.'}, status=status.HTTP_403_FORBIDDEN)

        else:
            return response.Response({'message': 'Invalid email. Please enter a valid email.'}, status=status.HTTP_400_BAD_REQUEST)


        return response.Response({'message': 'Confirmation code sent.'}, status=status.HTTP_200_OK)

class ConfirmEmailCodeView(views.APIView):
    serializer_class = serializers.ConfirmEmailCodeSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        code_serializer = serializers.ConfirmEmailCodeSerializer(data=request.data)
        queryset = models.ConfirmEmailNew.objects.all()

        if code_serializer.is_valid():
            ser_user = code_serializer.data.get('user')
            ser_code = code_serializer.data.get('code')

            # user = request.user
            
            if not queryset.filter(user=ser_user, code=ser_code).exists():
                return response.Response({'message': 'Code invalid try again.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                queryset.filter(user=ser_user).delete()
                return response.Response({'message': 'Code accepted. Email was verified succesfully.'}, status=status.HTTP_200_OK)

        else:

            # return response.Response({'message': 'Invalid user input.'})
            return response.Response(code_serializer.errors)

# class ResendCode(views.APIView):
#     serializer_class = serializers.ConfirmEmailSerializer

#     def post(self, request, *args, **kwargs):

#         # serializer_class = serializers.ConfirmEmailSerializer(data=request.data)
#         # code_serializer = serializers.ConfirmEmailSerializer(data=request.data)
#         queryset = models.ConfirmEmailNew.objects.all()


#         if serializer_class.is_valid():
#             ser_user = self.serializer_class.data.get('user')
#             # ser_code = code_serializer.data.get('code')

#             # user = request.user
            
#             if not queryset.filter(user=ser_user):
#                 queryset.filter(user=ser_user).delete()

#                 return response.Response({'message': 'Verification code was resent.'}, status=status.HTTP_200_OK)
#             else:
#                 return response.Response({'message': 'Unable to resent code.'}, status=status.HTTP_400_BAD_REQUEST)

                







    



    # def post(self, request, *args, **kwargs):

    #     id = self.kwargs.get('pk')

    #     product = self.get_queryset()
    #     user = request.user
    #     # body = 'Client ({}) is interested in the selected product {}'.format(user.first_name, product[id-1])
    #     context = ({
    #         'first_name': user.first_name,
    #         'last_name' : user.last_name,
    #         'email' : user.email,
    #         'phone_no': user.phone_no,
    #         'gender': user.gender,
    #         'dob': user.dob,
    #         'home_address': user.home_address,
    #         'location': user.location,
    #         'employee_number': user.employee_number,
    #         'trn': user.trn,
    #         'employer': user.employer,
    #         'product': product[id-1].title,
    #     })

    #     print('Test content {}'.format(context))
     
    #     try:

            
    #         self.send_email(request, context, user)
    #         return response.Response({'message': 'email was sent'})
    #     except:
    #         return response.Response({'message': 'Oops something went wrong!!!'})












class TestAPIView(views.APIView):

    serializer_class = serializers.TestSerializer

    def get(self, request, format=None):

        api_test = [
            "testing this shit",
            "this is pretty cool"
        ]
        return response.Response(
            {
                'message': 'Hello',
                'api_test': api_test
            }
        )


    def post(self, request):
        # create hello name with full name
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            fname = serializer.validated_data.get('fname')
            lname = serializer.validated_data.get('lname')
            message = fname + ' ' + lname

            return response.Response({'message': message})
        else:
            return response.Response(
                serializer.error,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        # update an object
        return response.Response({'method': 'PUT'})
    
    def delete(self, request, pk=None):
        # delete an object
        return response.Response({'method': 'DELETE'})
    
    def patch(self, request, pk=None):
        # partial update an object
        return response.Response({'method': 'PATCH'})


class TestViewset(viewsets.ViewSet):

    serializer_class = serializers.TestSerializer
    

    def list(self, request):
        api_info = [
            "method types: List, Create, Retrieve, etc",
            "Testing this crap",
            'Testing'
        ]
        return response.Response({'message': api_info})

    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            fname = serializer.validated_data.get('first_name')
            lname = serializer.validated_data.get('last_name')
            message = fname + " " + lname
            return response.Response({'message': message})
        else:
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        return response.Response({'method': 'GET'})
    


# class test2APIView(viewsets.ModelViewSet):

#     queryset = models.User.objects.all()
#     serializer_class = serializers.Test2Serializer

#     # serializer_class = serializers.Test2Serializer

#     # def get(self, request, format=None):

#     #     serializerInfo = self.serializer_class(data=request.data)
#     #     fname = serializerInfo.validated_data.get('')

#     #     return Response({'info': serializerInfo})
