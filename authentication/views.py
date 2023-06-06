from rest_framework.response import Response
from rest_framework.views import APIView

from knox.models import AuthToken

from .serializers import registerNewUserSerializer

# Create your views here.

class registerNewUserView(APIView):
    
    def post(self, request):
        serializer = registerNewUserSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            #save the user instance from request
            user = serializer.save()
            
            #create a new token with the user instance
            token = AuthToken.objects.create(user)[1]
            
            data = {
                'message': 'User created successfully',
                'token': token
            }
            return Response(data)
        
        return Response(serializer.errors, status=400)
