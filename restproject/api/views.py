from django.shortcuts import render
from  rest_framework.views import APIView
from .serializer import UserCustomModelSerializer,UserProfileSerilizer,DoctorListSerializer,AdminSerializer
from . models import UserCustomModel, Doctor
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import LoginSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import MyTokenObtainPairSerializer

class Register(APIView):
    def post(self, request, format=None):
        serializer = UserCustomModelSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            password = serializer.validated_data.get('password')
            is_doctor = serializer.validated_data.get('is_doctor')
            user = UserCustomModel.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_doctor=is_doctor,
            )
            if is_doctor:
                Doctor.objects.create(user=user)

            return Response({'msg': 'Data inserted, Registration Successful.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
from django.contrib.auth import authenticate


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print(email,'email')
            password = serializer.validated_data['password']
            print(password,'password')
            
            user = authenticate(email=email, password=password)
            print(user,'userrrrrr')
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
@authentication_classes([JWTAuthentication])
class Userprofile(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request,format = None):
        
        
        user_profile = UserCustomModel.objects.get(id=request.user.id)
        serializer = UserProfileSerilizer(user_profile)
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request):
        try:
            user_update = request.user
           
            serializer = UserProfileSerilizer(user_update,data = request.data,partial = True)   
            
            if serializer.is_valid():
                serializer.save()
                print(serializer.data,'kk')
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg': 'Invalid data provided'},status=status.HTTP_404_NOT_FOUND)
        except UserCustomModel.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'msg': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

    def delete(self, request, user_id):
            user = get_object_or_404(UserCustomModel,id=user_id)
            user.delete()
            return Response({'msg': 'User profile deleted successfully'})
                
  
       
       
       
class DoctorsViewlist(APIView):
    def get(self,request,format =None):
        doctor = UserCustomModel.objects.filter(is_doctor = True)
        serializer = DoctorListSerializer(doctor,many =True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
class AdminViewlist(APIView):
    
    def get(self,request,format =None):
        users = UserCustomModel.objects.all()
        serializer =AdminSerializer(users,many =True)
        return Response(serializer.data,status=status.HTTP_200_OK)  
    
    
    def patch(self, request, pk):
        print(pk)
        try:
            user = UserCustomModel.objects.get(id=pk)
            user.is_active = not user.is_active 
            user.save()
            serializer = AdminSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except UserCustomModel.DoesNotExist:
            return Response({'msg': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    
    
   
   
   
   
   
   
    
    
    
    
    
    
    

