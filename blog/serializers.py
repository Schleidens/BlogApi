from rest_framework import serializers

from PIL import Image
from io import BytesIO
from django.core.files import File

from django.utils.text import slugify
from random import randint

from .models import blogPost


class blogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = blogPost
        fields = '__all__'
        
    
    # def compress_image(self, img):
    #     if img:
    #         # Open the image using Pillow
    #         image = Image.open(img)
            
    #         #Resize the image to a maximum size of 1024 x 1024 pixels
    #         image.thumbnail((1024, 1024))
            
    #         # Compress the image
    #         if img.name.lower().endswith('.jpg') or img.name.lower().endswith('.jpeg'):
    #             format = 'JPEG'
    #             # Set the JPEG quality level to 80%
    #         elif img.name.lower().endswith('.png'):
    #             format = 'PNG'
    #             # Set the PNG compression level to 6 (out of 9)
    #             image = image.convert('P', palette=Image.ADAPTIVE, colors=256)
    #             options = {'compress_level': 6}
    #         else:
    #             # Unsupported image format
    #             raise serializers.ValidationError("Format not supported")
            
    #         output = BytesIO()
    #         image.save(output, format=format, optimize=True, quality=80, **options if format == 'PNG' else {})
    #         new_image = File(output, name=img.name)

    #         # Set the image field to the compressed image
    #         img = new_image
            
    #         return img
        
    # def validate_slug(self, data):
    #     title = data.get('title')
    #     slug = slugify(title)
        
    #     if blogPost.objects.filter(slug=slug).exists():
    #         slug = slug + "-" + str(randint(1000, 9999))
            
    #     return slug
        
        
    # def create(self, validated_data):
    #     cover = validated_data.get('cover')
        
    #     if cover:
    #         compressed_image = self.compress_image(cover)
    #         validated_data['image'] = cover
    #     return super().create(validated_data)
    
    
    # def update(self, validated_data):
    #     cover = validated_data.get('cover')
        
    #     if cover:
    #         compressed_image = self.compress_image(cover)
    #         validated_data['image'] = cover
    #     return super().update(validated_data)