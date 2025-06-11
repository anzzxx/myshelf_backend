from rest_framework import serializers
from .models import Accounts
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



class SignupSerilizer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(write_only=True, required=True)
    
    
    class Meta:
        model=Accounts
        fields=("username","email","password","first_name","last_name","phone_number")
        extra_kwargs={"username":{'required':False}}
        
    def validate_email(self,value):
        if Accounts.objects.filter(email=value).exists():
            raise serializers.ValidationError("this must be unique.")
        return value
    
    def validate_password(self,value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        return value        
    
    def create(self,validate_data):
        email=validate_data.get("email")
        password=validate_data.get("password")
        username=validate_data.get("username",None)
        first_name=validate_data.get("first_name",None)
        last_name=validate_data.get("last_name",None)
        phone_number=validate_data.get("phone_number",None)
        user=Accounts.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        return user
    
class CustomLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)    
    
    def validate(self,data):
        email=data.get("email")
        password=data.get("password")
        
        user=authenticate(email=email,password=password)
        
        if user is None:
            raise serializers.ValidationError({"detail": "Invalid email or password"})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "Account is inactive"})
        refresh=RefreshToken.for_user(user)
        
        return{
            "message":"Login successful!",
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        }
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Accounts
        fields=["id","email","first_name","last_name","phone_number","profile_image"]
            
class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['first_name', 'last_name', 'phone_number',"profile_image"]
        extra_kwargs = {
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile_image': {'required': False},
        }            