from django.urls import path, include
from rest_framework import routers

from .views import blogViewset, commentViewset

router = routers.SimpleRouter()

router.register(r'blogs', blogViewset)
router.register(r'comments/(?P<blog_id>\d+)', commentViewset)

urlpatterns = [
    path('', include(router.urls))
]

