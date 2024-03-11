from rest_framework import serializers
from django.contrib.auth.models import  User
from django.contrib.auth import authenticate
from  rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.Serializer):
    f_name=serializers.CharField()
    l_name=serializers.CharField()
    
    username=serializers.CharField()
    password=serializers.CharField()
    
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("username already exists")
        
        return data  
        
    def create(self,validated_data):
        user=User(first_name=validated_data['f_name'],last_name=validated_data['l_name'],username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    
    def validate(self, attrs):
        if not User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("you are not a user create account first")
        return attrs
        
        
        
    def get_token(self,data):
        user=authenticate(username=data['username'],password=data['password'])
            
        if not user:
            return{"msg":("invalid credentials")}
        token=RefreshToken.for_user(user)
        return {
            'data':{'token':str(token),'access':str(token.access_token)},
        }

    
