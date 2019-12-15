from django.urls import path

from .views import (
    RegisterUserView,
    LoginUserView,
    LogoutView,
    RefreshTokenView
)

app_name = 'authentication'
urlpatterns = [
    path(r'signup', RegisterUserView.as_view(), name='signup'),
    path(r'login', LoginUserView.as_view(), name='login'),
    path(r'logout', LogoutView.as_view(), name='logout'),
    path(r'refresh', RefreshTokenView.as_view(), name='user-detail'),
]
