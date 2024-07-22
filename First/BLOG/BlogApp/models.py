from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    roles = (
        ('author' ,'Author'),
        ('reader', 'Reader')
    )
    user_type = models.CharField(max_length=10,choices=roles)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profiles')

    def __str__(self):
        return f'{self.user}-{self.user_type}'

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    roles = (
        ('author' ,'Author'),
        ('reader', 'Reader')
    )
    user_type = models.CharField(max_length=10,choices=roles)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profiles')

    def __str__(self):
        return f'{self.user}-{self.user_type}'

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    creator = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}--{self.creator}'
    
