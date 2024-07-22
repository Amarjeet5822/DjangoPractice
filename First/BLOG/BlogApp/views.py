from django.shortcuts import render
from BlogApp.models import Profile,Post
from django.contrib.auth.models import User
from .serializers import PostSerializer,UserSerializer,ProfileSerializer

from rest_framework.decorators import APIView
from rest_framework.response import Response 
from rest_framework import status


# Create your views here.
class RegistrationView(APIView):
    # authentication_classes = [AllowAny]

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        print("before checking",serializer)
        if serializer.is_valid():
            print("before checking",serializer)
            user = serializer.save()
            profile = Profile(user=user,user_type=request.data.get('user_type'))
            profile.save()
            return Response({'message':'Signup Successfull'},status=status.HTTP_201_CREATED)
        return Response({'message':'Username or Password is invalid. Enter correctly'},status=status.HTTP_400_BAD_REQUEST)
    