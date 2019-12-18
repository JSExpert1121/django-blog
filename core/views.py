from django.shortcuts import render
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from .mailers import send_verification_mail
from .sms import send_verification_sms

# Create your views here.
@api_view(['GET'])
def send_mail(request):

    params = request.query_params
    client = settings.CLIENT_URL
    sec_token = params.get('sec_token', None)
    username = params.get('username', None)
    to = params.get('to', None)

    if not sec_token:
        raise ValueError('Invalide token')

    if not username:
        raise ValueError('Invalide username')

    if not to:
        raise ValueError('Invalide to address')

    result = send_verification_mail(sec_token, to, username)
    print('Sendmail result {}'.format(result))

    return Response({
        "Status": "Mail sent"
    }, status.HTTP_200_OK)


@api_view(['GET'])
def send_sms(request):

    params = request.query_params
    code = params.get('code', None)
    to = params.get('to', None)

    if not code:
        raise ValueError('Invalide token')

    if not to:
        raise ValueError('Invalide to address')

    result = send_verification_sms(int(code), to)
    print('Send SMS result {}'.format(result))

    return Response({
        "Status": "SMS sent"
    }, status.HTTP_200_OK)
