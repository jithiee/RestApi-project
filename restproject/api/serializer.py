from rest_framework import serializers
from . models import UserCustomModel,Doctor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError


class UserCustomModelSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    # is_doctor = serializers.BooleanField(default=False,required=False)
    # email = serializers.EmailField()
    
    class Meta:
          model = UserCustomModel
          fields = ['id','username','email','password','is_doctor','password2']
        
        
    def validate(self,data):
        
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password Does Not Match')
        return data     
    
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()    


    
    
class UserProfileSerilizer(serializers.ModelSerializer):
    class Meta:
        model = UserCustomModel
        fields = ['username', 'email','first_name','last_name']
        
    

    # def update(self, instance, validated_data):
        
    #     # instance == UserCustomModel
    #     # UserCustomModel.first_name = validated_data.get('first_name', instance.first_name)  # we can like this
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     return instance
    
class DoctorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Doctor
            fields = ['user','hospital','department']
    
class AdminSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserCustomModel
            fields = ['id','username','email','is_doctor','first_name','last_name']
            
    

