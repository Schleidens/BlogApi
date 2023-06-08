from django.urls import path, include
from rest_framework import routers

from .views import blogViewset

router = routers.SimpleRouter()

router.register(r'blogs', blogViewset)

urlpatterns = [
    path('', include(router.urls))
]

