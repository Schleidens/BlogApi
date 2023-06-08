from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from knox.auth import TokenAuthentication


from .serializers import blogSerializer
from .models import blogPost

# Create your views here.
    
    
class blogViewset(ModelViewSet):
    serializer_class = blogSerializer
    queryset = blogPost.objects.all()
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    

