from rest_framework import serializers
from . models import UserCustomModel,Doctor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_admin'] = user.is_admin
        token['is_active'] =user.is_active
        return token
    
    
class UserCustomModelSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model = UserCustomModel
        fields = ['id', 'username', 'email', 'password', 'is_doctor', 'password2', 'first_name', 'last_name']

        
    def validate(self,data):
        
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password Does Not Match')
        return data     




class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()    


class DoctorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Doctor
            fields = ['hospital','department']
    
class UserProfileSerilizer(serializers.ModelSerializer):
    doctorprofile = DoctorSerializer()
    class Meta:
        model = UserCustomModel
        fields = ['username', 'first_name', 'last_name', 'email', 'doctorprofile']
   
   


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name )
        instance.last_name = validated_data.get('last_name',instance.last_name )
        instance.email = validated_data.get('email',instance.email )
        doctor_data = validated_data.get('doctorprofile',{})
        if doctor_data:
            doctor = instance.doctorprofile
            doctor.hospital = doctor_data.get('hospital',doctor.hospital)
            doctor.department = doctor_data.get('department',doctor.department)
            doctor.save()
        instance.save()
        return instance
            
        
        
class DoctorListSerializer(serializers.ModelSerializer):
    doctorprofile = DoctorSerializer()

    class Meta:
        model = UserCustomModel
        fields = ['username', 'first_name', 'last_name', 'doctorprofile']

    
    
class AdminSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserCustomModel
            fields = ['id','username','email','is_doctor','first_name','last_name','is_active','is_admin']
            
    

