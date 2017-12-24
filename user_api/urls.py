from django.urls import path, include
from user_api.views import UserView, UserDetailView

urlpatterns = [
    path('', UserView.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('<int:pk>/', UserDetailView.as_view()),
]
