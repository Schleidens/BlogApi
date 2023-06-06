from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class registerNewUserSerializer(serializers.ModelSerializer):
    #add a confirm password field
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'first_name', 'last_name']
        
    #make sure password and password_confirm match by validating them
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        
        #check if they both match
        if password != password_confirm:
            raise serializers.ValidationError('Password and Confirm Password do not match.')
        return data
    
    #redefine the save(create) methods
    def create(self, validated_data):
        
        #create the user instance
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user