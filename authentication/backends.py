from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.conf import settings

from .models import User
from datetime import datetime
import jwt


class JWTAuthentication(BaseAuthentication):
    authentication_type = 'Bearer'

    def authenticate(self, request):

        # initialize request.user
        request.user = None

        auth_header = get_authorization_header(request).split(b' ')
        auth_type = self.authentication_type.lower()

        if len(auth_header) == 1 or len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8').lower()
        token = auth_header[1].decode('utf-8')

        if prefix != auth_type:
            return None

        return self._authenticate_jwt(request, token)

    def _authenticate_jwt(self, request, token):

        try:
            payload = jwt.decode(token, settings.JWT_SECRETE_KEY)
        except:
            raise exceptions.AuthenticationFailed('Invalid token')

        expired = payload.get('expired', None)
        if not expired:
            raise exceptions.AuthenticationFailed('Invalid token format')

        # print('{}'.format(payload['id']))
        try:
            user = User.objects.get(pk=payload['id'])
        except:
            raise exceptions.AuthenticationFailed('Invalid User ID')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Deactivated user')

        expired_time = datetime.strptime(expired, '%Y-%m-%d %H:%M:%S.%f')

        if datetime.now() > expired_time:
            raise exceptions.AuthenticationFailed('Token is expired')

        return (user, None)
