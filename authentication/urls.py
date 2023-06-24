from django.urls import path

from .views import registerNewUserView, loginUserView
from knox.views import LogoutView

urlpatterns = [
    path('register/', registerNewUserView.as_view()),
    path('login/', loginUserView.as_view()),
    path('logout/', LogoutView.as_view())
]
