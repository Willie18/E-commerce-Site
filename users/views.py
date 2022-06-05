from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from . import serializers
from .utils import get_and_authenticate_user,create_user_account
from django.contrib.auth import get_user_model, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    queryset=User.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register':serializers.UserRegisterSerializer,
        'password_change': serializers.PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request,format=None):
        """
        ``POST`` Generates a request to Login a user

        Request POST api/v1/auth/login

        Payload
        {
            "username":"user1",
            "password":"password"
        }

        Response
        {
            "id": int,
            "email": "string,
            "username": "string",
            "is_active": boolean,
            "is_staff": boleans,
            "auth_token": "string(uuid)"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False)
    def register(self, request,format=None):
        """
        ``POST`` Generates a request to create a user

        Request POST api/v1/auth/register

        Payload
        {
            "username":"user1",
            "email":"test@bar.com",
            "password":"password"
        }

        password should have atleast 8 characters
        email and username should be unique
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validate_email(serializer.validated_data.get("email",None))
        serializer.validate_username(serializer.validated_data.get("username",None))
        user = create_user_account(**serializer.validated_data)
        user.is_Active=True
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request,format=None):
        """
        ```POST`` Generates a request to Logout the user

        Request  POST  api/v1/auth/logout
        """        
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    # @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    # def password_change(self, request,format=None):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     request.user.set_password(serializer.validated_data['new_password'])
    #     request.user.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


@api_view()
def AuthRootView(request):
    """
    ```GET`` List the actions exposed by the endpoint

        Request: GET api/v1/auth

        Response object of the uri the endpoint exposes
    """
    routes={
        "login":f"{request.build_absolute_uri()}login",
        "register":f"{request.build_absolute_uri()}register",
        "logout":f"{request.build_absolute_uri()}logout" 
    }
    return Response(data=routes,status=status.HTTP_202_ACCEPTED)


# class UserViewSet(CreateModelMixin,viewsets.GenericViewSet):
#     serializer_class=UserRegistrationSerializer
#     queryset=CustomerUser.objects.all()
#     def create(self, request, *args, **kwargs):
#         serializer=self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # super().create(request, *args, **kwargs)(self,request)
#             return Response(
#                 {"RequestId":str(uuid4()),
#                 "Message":"User Created Successfully",
#                 "User":serializer.data},status=status.HTTP_201_CREATED)
#         return Response({"Errors":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
# class Logout(APIView):
#     def get(self, request, format=None):
#         # simply delete the token to force a login
#         request.user.auth_token.delete()
#         return Response({"message":"User logout successfully"},status=status.HTTP_200_OK)

# @api_view(['POST'])
# def registration_view(request, format=None):
#     """
#     user registration
#     """ 
#     #user registration
#     data = {}
#     if request.method == 'POST':
#         serializer = UserRegistrationSerializer(data=request.data)
    
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = "User created successfully"
#             token = Token.objects.get(user=user).key
#             data['token'] = token
#             return Response(data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def logout(request, format=None):
#     #user logout
#     request.user.auth_token.delete() #deletes token
#     return Response(status=status.HTTP_200_OK)

# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'register': reverse('register', request=request, format=format),
#         'login': reverse('login', request=request, format=format),
#         'logout': reverse('logout', request=request, format=format),
#     })