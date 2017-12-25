from django.urls import path
from user_api.views import UserView, UserDetailView, LoginView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<uuid:user_id>/', UserDetailView.as_view()),
    path('sessions/', LoginView.as_view()),
]
