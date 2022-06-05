from django.contrib.auth import get_user_model,password_validation
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager




User=get_user_model()

# validate our input
class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

# provide the response
class AuthUserSerializer(serializers.HyperlinkedModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
         model =User
         fields = ('id', 'email', 'username', 'is_active', 'is_staff','auth_token')
         read_only_fields = ('id', 'is_active', 'is_staff')
    
    def get_auth_token(self, obj):
        try:
            token = Token.objects.get(user_id=obj.id)
        except Token.DoesNotExist:
            token = Token.objects.create(user=obj)
        # token = Token.objects.create(user=obj)
        return token.key
class EmptySerializer(serializers.Serializer):
    class Meta:
        ref_name="logout"
    pass

class UserRegisterSerializer(serializers.HyperlinkedModelSerializer):
    """
    A user serializer for registering the user
    """
    username=serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('id','username','email', 'password',)

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)
    
    def validate_username(self,value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("Username is already taken")
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

class PasswordChangeSerializer(serializers.HyperlinkedModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        fields=["current_password","new_password"]
        model=User

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


# class UserRegistrationSerializer(serializers.ModelSerializer):
#     email=serializers.CharField(max_length=50,min_length=5)
#     password=serializers.CharField(max_length=150,write_only=True)
#     username=serializers.CharField(max_length=50,write_only=True)    
#     class Meta:
#         model = CustomerUser
#         fields = ['username','email','password']
#         extra_kwargs = {'password': {'write_only':True, 'style':{'input_type':'password'}}}
#         read_only_fields = ('email',)
#     def validate(self,args):
#         # print(args)
#         email=args.get("email",None)
#         username=args.get("username",None)
#         if self.Meta.model.objects.filter(email=email).exists():
#             raise serializers.ValidationError({'email':'Email already exists'})
#         if CustomerUser.objects.filter(username=username).exists():
#             raise serializers.ValidationError({'username':'Username already exists'})
#         return super().validate(args)
#     # create User
#     def create(self,validated_data):
#         user=CustomerUser(
#             username=validated_data["username"],
#             email=validated_data["email"],
#             password=validated_data["password"]
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
        # #Extract Password
        # password=validated_data.pop("password",None)

        # #Assign the `CustomerUser` models data to `instance` object
        # instance=self.Meta.model(**validated_data)

        # if password is not None:
        #     instance.set_password(password)
        # instance.save()
        # return instance

    # def Update(self,instance,validated_data):
    #     for attr,value in validated_data.items():
    #         if attr=="password":
    #             instance.set_password(value) #apply the set_password function
    #         else:
    #             setattr(instance,attr,validated_data) #apply the instance with new value
    #     instance.save()
    #     return instance



        



    

