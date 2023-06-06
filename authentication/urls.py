from django.urls import path

from .views import registerNewUserView

urlpatterns = [
    path('register/', registerNewUserView.as_view())
]
