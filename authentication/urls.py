from django.urls import path

from .views import registerNewUserView, loginUserView

urlpatterns = [
    path('register/', registerNewUserView.as_view()),
    path('login/', loginUserView.as_view())
]
