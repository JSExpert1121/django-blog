from django.urls import path

from .views import UserDetailView

app_name = 'account'
urlpatterns = [
    path(r'setting', UserDetailView.as_view(), name='user-setting')
]
