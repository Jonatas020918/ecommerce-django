from django.urls import path
from .views import UserRegistrationView, UserListView, UserDetailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail')
]