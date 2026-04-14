from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
import uuid

user = get_user_model()

class Media(models.Model):
    file = models.FileField(upload_to='posts/%Y/%m/%d/',null=True,blank=True,validators=FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','mp4','webp']))
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    media = models.ManyToManyField(Media,blank=True,related_name='posts')
    author = models.ForeignKey(user,on_delete=models.CASCADE,related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Tweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=False,null=False)
    author = models.ForeignKey(user,on_delete=models.CASCADE,related_name='tweets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

