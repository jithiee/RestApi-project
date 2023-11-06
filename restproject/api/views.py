from django.shortcuts import render
from  rest_framework.views import APIView
from .serializer import UserCustomModelSerializer,UserProfileSerilizer,DoctorSerializer,AdminSerializer
from . models import UserCustomModel, Doctor
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated


class Register(APIView):
    def post(self, request, formate=None):
        serializer = UserCustomModelSerializer(data = request.data)
        if serializer.is_valid():
            email = serializer._validated_data.get('email')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            is_doctor = serializer.validated_data.get('is_doctor')
            user=UserCustomModel.objects.create_user(
                email = email,
                username = username,
                password = password,
                is_doctor = is_doctor,
            )
            if user.is_doctor:
                Doctor.objects.create(user=user)
            
            return Response({'msg':'data inserted , Registration Succesfull..'},status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
from django.contrib.auth import authenticate





class Login(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
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
    # authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request,format = None):
        
        
        user_profile = UserCustomModel.objects.get(id=request.user.id)
        serializer = UserProfileSerilizer(user_profile)
        print(serializer)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def patch(self,request):
        try:
            user_update = UserCustomModel.objects.get(id=request.user.id )
            print(request.data)
            serializer = UserProfileSerilizer(user_update,data = request.data,partial = True)   
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'msg': 'Invalid data provided'},status=status.HTTP_404_NOT_FOUND)
        except UserCustomModel.DoesNotExist:
            return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
        # Catch any unexpected exceptions and handle them appropriately.
            return Response({'msg': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    
    def delete(self,request):
        try:
            user_del = UserCustomModel.objects.get(id=request.user.id)
            serializer = UserProfileSerilizer(user_del,data= request.data)
            if serializer.is_valid():
                user_del.delete()
                return Response({'msg': 'User profile deleted successfully'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        except UserCustomModel.DoesNotExist:
           return Response({'msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
       
class DoctorsViewlist(APIView):
    def get(self,request,format =None):
        doct = Doctor.objects.all()
        serializer = DoctorSerializer(doct,many =True)
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
    
   
   
   
   
   
   
    
    
    
    
    
    
    

   
# class UserAPIView(APIView):
#     def post(self,request,*args, **kwargs):
#         serializer=UserProfileSerilizer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data.get("email")
#             password=serializer.validated_data.get("password")
#             user=authenticate(request,email=email,password=password)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
