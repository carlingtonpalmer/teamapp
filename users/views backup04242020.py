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
from django.core.mail import EmailMessage
from django.conf import settings
import json

# Create your views here.

class UserViewset(generics.ListAPIView):
    """ this class is use for creating and updating users """

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all() # just tell django we gonna use CREATE, UPDATE, RETRIEVE LIST ETC.
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.ModifyOwnProfile,)
    # filter_backends = (filters.SearchFilter, )
    # search_fields = ('email', 'first_name', 'last_name',)
    # token, created = Token.objects.get_or_create(user=user)
    # response.Response({"token": token.key})
    




class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserUpdateSerializer
    queryset = models.User.objects.all()



# class ProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Profile.objects.all()
#     serializer_class = serializers.UserProfileSerializer

# class ProfileCreateView(generics.ListCreateAPIView):
#     queryset = models.Profile.objects.all()
#     serializer_class = serializers.UserProfileSerializer



    
class LoginUserApiView(ObtainAuthToken):

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

    def post(self, request,*args, **kwargs):
        logout(request)
        return response.Response(
            {
                "message" : "User was logged out successfully."
            }
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
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            


class ProductCategoryView(generics.ListAPIView): # new changes 14/02/202
    serializer_class = serializers.ProductCategorySerializer
    queryset = models.ProductCategory.objects.all()
    
    
class ProductSubCategoryDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSubCatergorySerializer
    queryset = models.ProductSubCategory.objects.all()



class ProductSubCategoryListSlugView(generics.ListAPIView):
    serializer_class = serializers.ProductSubCatergorySerializer
    
    def get_queryset(self):
        queryset = models.ProductSubCategory.objects.all()
    
        slug = self.kwargs.get('slug', None)
        # print('Slug: {}'.format(slug))
        
        queryset = queryset.filter(prod_id_id__slug=slug)
        # queryset = models.ProductSubCategory.objects.filter(slug=slug)#.values_list()

        return queryset



class SingleProductView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSubCatergorySerializer

    def get_queryset(self):
        queryset = models.ProductSubCategory.objects.all()
  
        id = self.kwargs.get('pk', None) #getting values from browser
        slug = self.kwargs.get('slug', None)
        # print('ID: {}'.format(id))

        queryset = queryset.filter(prod_id_id__slug=slug)
        # for q in queryset:

        # print('title: {}'.format(queryset[id]))
        # self.send_email1(self,request)
        return queryset


    def post(self, request, *args, **kwargs):

        id = self.kwargs.get('pk')
        # print('ID: {}'.format(id))
        
        product = self.get_queryset()
        # print("Prod id: {}".format(product))
        # print("Prod id: {}".format(product[id]))
        # print("Prod id: {}".format(product[id-1]))
        user = request.user
        body = 'Client ({}) is interested in the selected product {}'.format(user.first_name, product[id-1])
        print(body)
        message = "Good day Admin, \n\n{}: \nName: {} {}\nEmail:{}\nDOB:{}\nGender:{}\nPhone number:{}\nHome Address:{}\nLocation:{}\nEmployee #:{}\nTRN: {}\nEmployer: {}"#\nRegulation #:{}\nRank:{}
        message_with_values = message.format(body, user.first_name, user.last_name, user.email, user.dob, user.gender,user.phone_no,user.home_address, user.location, user.employee_number, user.trn, user.employer)#, user.regulation_number, user.rank
        
        email_from = settings.EMAIL_HOST_USER
        to = ['teamappdev2019@gmail.com', ]#to some admin user
        try:
            email = EmailMessage('Product Alert!!!', message_with_values, email_from, to)
            email.send(fail_silently=False)
            return response.Response({'message': 'email was sent'})
        except:
            return response.Response({'message': 'Oops something went wrong!!!'})















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
