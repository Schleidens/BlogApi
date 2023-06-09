from django.urls import path, include
from rest_framework import routers

from .views import blogViewset, commentViewset, UserBlogViewset

router = routers.SimpleRouter()

router.register(r'blogs', blogViewset)
router.register(r'comments/(?P<slug>[-\w]+)', commentViewset)
router.register(r'user-blogs', UserBlogViewset)

urlpatterns = [
    path('', include(router.urls))
]

