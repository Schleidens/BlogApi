from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from PIL import Image
from io import BytesIO
from django.core.files import File

from django.utils.text import slugify
from random import randint

from .models import blogPost


#set serializer for post request on blogPost
class postBlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = blogPost
        fields = ['cover', 'title', 'content']
        
#set serializer for get request on blogPost
class getBlogSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()
    
    class Meta:
        model = blogPost
        fields = '__all__'
        
    def get_author(self, obj):
        author = obj.author
        return {
            'id': author.id,
            'username': author.username,
            'full-name': f'{author.first_name} {author.last_name}',
            'email': author.email
        }