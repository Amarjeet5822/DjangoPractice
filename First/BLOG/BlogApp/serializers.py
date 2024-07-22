from rest_framework import serializers
from .models import Post,Profile
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError,AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username', 'password']
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self,validated_data):
        instance = self.Meta.model(**validated_data)
        password = validated_data.pop('password',None)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
        # else:
        #     raise ValidationError({'message':'password field is required'})


class ProfileSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Profile
        fields = ['user','user_type']

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


    