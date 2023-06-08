from django.db import models
from django.conf import settings

# Create your models here.


class blogPost(models.Model):
    cover = models.ImageField(upload_to='blog', blank=True, null=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField(default="", unique=True, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title