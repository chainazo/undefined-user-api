from django.urls import path
from user_api.views import UserView, UserDetailView

urlpatterns = [
    path('', UserView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
]
