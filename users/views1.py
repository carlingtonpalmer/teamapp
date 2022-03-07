from rest_framework import response
from rest_framework import status #, viewsets
from users import serializers, models, permissions
from rest_framework import viewsets, filters,generics, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated, AllowAny
import json

# Create your views here.

class UserViewset(viewsets.ModelViewSet):
    """ this class is use for creating and updating users """

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all() # just tell django we gonna use CREATE, UPDATE, RETRIEVE LIST ETC.
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.ModifyOwnProfile,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('email', 'first_name', 'last_name',)   
    # token, created = Token.objects.get_or_create(user=user)
    # response.Response({"token": token.key})
    




class UserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()



class ProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.UserProfileSerializer

class ProfileCreateView(generics.ListCreateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.UserProfileSerializer



    
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
            'token': token.key
        })

class LogoutUserView(views.APIView):

    def post(request):
        logout(request)
        return response.Response(
            {
                "message" : "User was logged out successfully."
            }
        )


class CreateUserView(generics.ListCreateAPIView):

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all() # just tell django we gonna use CREATE, UPDATE, RETRIEVE LIST ETC.
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.ModifyOwnProfile,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('email', 'first_name', 'last_name',) 

    def post(self, request):
        id = request.POST.get('id')
        fn = request.POST.get('first_name')
        ln = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = models.User.objects.create_user(fn, ln, email,password)
        token = Token.objects.create(user=user)

        return response.Response({
            'id' : user.id,
            'first_name': user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'token': token.key
        })




# class LogoutView(APIView):
#     """
#     Calls Django logout method and delete the Token object
#     assigned to the current User object.

#     Accepts/Returns nothing.
#     """
#     permission_classes = (AllowAny,)

#     def get(self, request, *args, **kwargs):
#         if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
#             response = self.logout(request)
#         else:
#             response = self.http_method_not_allowed(request, *args, **kwargs)

#         return self.finalize_response(request, response, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.logout(request)

#     def logout(self, request):
#         try:
#             request.user.auth_token.delete()
#         except (AttributeError, ObjectDoesNotExist):
#             pass

#         django_logout(request)

#         return Response({"detail": _("Successfully logged out.")},
#                         status=status.HTTP_200_OK)


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
