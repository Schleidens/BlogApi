from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, serializers, status
from rest_framework.response import Response

from knox.auth import TokenAuthentication


from .serializers import blogSerializer
from .models import blogPost

# Create your views here.
    
    
class blogViewset(ModelViewSet):
    serializer_class = blogSerializer
    queryset = blogPost.objects.all()
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    #override the save methods
    def perform_create(self, serializer):
        
        #return error if a user try to send data as a non authenticated user
        user = self.request.user
        if serializer.validated_data['author'] != user:
            raise serializers.ValidationError(
                {"error": "User mismatch. The 'author' field must be the authenticated user."}
                )
        
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