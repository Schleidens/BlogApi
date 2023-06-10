from django.contrib import admin

from .models import blogPost, blogComment

# Register your models here.

admin.site.register(blogPost)
admin.site.register(blogComment)