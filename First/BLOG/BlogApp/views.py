from django.shortcuts import render
from BlogApp.models import Profile,Post
from django.contrib.auth.models import User
from .serializers import PostSerializer,UserSerializer,ProfileSerializer
from django.contrib.auth import logout,login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import APIView
from rest_framework.response import Response 
from rest_framework import status
import jwt,datetime

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
    
class Loginview(APIView):
    
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        # user = authenticate(username=username,password=password)
        user = User.objects.filter(username=username).first()
        print('It is',user)
        if user is  None:
            return Response({'msg':'Not registerd User! Please signup,'},status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            raise AuthenticationFailed({'msg':"check password"})
        login(request,user)
        payload = {
            'id':user.id,
            'iat':datetime.datetime.now(datetime.UTC),
            'exp':datetime.datetime.now(datetime.UTC)+datetime.timedelta(minutes=120) 
        }
        token = jwt.encode(payload,'cap01_046',algorithm='HS256')
        response = Response()
        response.data = {'msg':'login Successfull','token':token}
        response.status = status.HTTP_200_OK
        response.set_cookie(
            key = 'jwt',
            value = token,
            httponly= False,
            samesite= None,
            secure=None
        )

        return response
    
class LogoutView(APIView):

    def post(self,request):
        logout(request)
        response = Response()
        response.data = {'msg':'logout Successfully'}
        response.status = status.HTTP_200_OK
        response.delete_cookie('jwt')
        return response

class PostListView(APIView):

    def get(self,reqeust):
        blogs = Post.objects.all()
        serializer = PostSerializer(blogs,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        request.data['creator']= request.creator.id
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Post added'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class PostDetailView(APIView):
    def getObject(self,pk):
        try :
            blog = Post.objects.get(id=pk)
            return blog
        except Post.DoesNotExist :
            return Response({'message': 'Blog not Exist!!'})


    def get(self,request,pk):
        blog = self.getObject(pk)
        serializer = PostSerializer(blog)
        return Response( serializer.data)
    
    def put(self,request,pk):
        blog = self.getObject(pk)
        serializer = PostSerializer(blog,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Post Updated'},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        blog = self.getObject(pk)
        blog.delete()
        return Response({'message': 'Post Deleted!!'})
    