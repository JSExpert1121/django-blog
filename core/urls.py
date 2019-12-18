from django.urls import path

from .views import send_mail, send_sms

app_name = 'core'
urlpatterns = [
    path(r'mail', send_mail, name='mail-test'),
    path(r'sms', send_sms, name='sms-test')
]
