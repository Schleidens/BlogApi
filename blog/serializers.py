from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from .models import blogPost, blogComment


#set serializer for post request on blogPost
class postBlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = blogPost
        fields = ['cover', 'title', 'content', 'draft']
        
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
        
        
'''
--------------------------------
serializer part for blog comment
--------------------------------
'''

#post comment serializer
class postCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = blogComment
        fields = ['content']
        
        
#get comment serializer
class getCommentSerializer(serializers.ModelSerializer):
    author = SerializerMethodField()
    
    class Meta:
        model = blogComment
        fields = '__all__'
        
    def get_author(self, obj):
        author = obj.author
        return {
            'id': author.id,
            'username': author.username,
            'full-name': f'{author.first_name} {author.last_name}',
        }