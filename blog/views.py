from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils.text import slugify
from random import randint

from knox.auth import TokenAuthentication


from .serializers import getBlogSerializer, postBlogSerializer
from .models import blogPost

# Create your views here.
    
    
class blogViewset(ModelViewSet):
    queryset = blogPost.objects.all()
    
    #set different serializer for both post and get request
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return getBlogSerializer
        elif self.request.method == 'POST':
            return postBlogSerializer
        else:
            return getBlogSerializer
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    
    
    #override the save methods
    def perform_create(self, serializer):
        
        #set the  author field to the authenticated user
        serializer.validated_data['author'] = self.request.user
        
        #return error if a user try to send data as a non authenticated user
        user = self.request.user
        if serializer.validated_data['author'] != user:
            raise serializers.ValidationError(
                {"error": "User mismatch. The 'author' field must be the authenticated user."}
                )
        
        '''
            fill the slug field with the current title turn into a slug
            and add random number if the slug already exist to make it unique
        '''
        title = serializer.validated_data['title']
        slug = slugify(title)
        
        if blogPost.objects.filter(slug=slug).exists():
            slug = slug + "-" + str(randint(1000, 9999))
            serializer.validated_data['slug'] = slug
        else:
            serializer.validated_data['slug'] = slug
        serializer.save()
        
    #return error if non authenticated user try deleting data as other user
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to delete this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    #return error if non authenticated user try modifying data as other user
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to update this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    #perform action for draft and undraft the blog post 
    @action(detail=True, methods=['put'])
    def set_draft(self, request, pk):
        instance = self.get_object()
        
        #make sure the request is from the authenticated user and return error if not
        if instance.author != request.user:
            return Response(
                {"error": "You do not have permission to update this post."},
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            instance.draft = not instance.draft
            instance.save()
            
            #set different message base on current draft value
            if instance.draft:
                message = 'Post set to draft'
            else:
                message = 'post has been published successfully'
            return Response({'message': message}, status=status.HTTP_200_OK)