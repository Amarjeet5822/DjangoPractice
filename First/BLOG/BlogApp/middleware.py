from django.urls import reverse,path
import jwt
from .models import Profile,Post
from rest_framework.exceptions import AuthenticationFailed
class JwtAuthMiddleware:
    
    def __init__(self,get_response):
        self.get_response = get_response
        self.excluded_path = [
        reverse('signup') ,reverse('login'), reverse('logout')
        ]
    
    def __call__(self,request):
        flag = False
        for excluded_path in self.excluded_path:
            if request.path.startswith(excluded_path):
                flag = True
                break
        flag_admin = request.path.startswith('/admin/')
        if flag or flag_admin:
            return self.get_response(request)
        
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token,'cap01_046',algorithms=['HS256'])
        # payload = {id,iat,exp}
        # user = User.objects.filter(id=payload['íd']).first()

        # if (user.profiles.user_type) != 'author':
        #     return AuthenticationFailed({'message':'Unauthorized'})
                    # OR
        profile = Profile.objects.filter(user = payload['id']).first()
        if profile.user_type!= 'author':
            return AuthenticationFailed({'message':'Unauthorized'})
        request.creator= profile 

        return self.get_response(request)