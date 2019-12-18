from twilio.rest import Client
from django.conf import settings


def send_sms(body, from_, to):
    client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

    return client.messages.create(
        body=body,
        from_=from_,
        to=to
    )


def send_verification_sms(code, to, from_=settings.ADMIN_PHONE):

    body = 'Your Django-blog verification code is %d' % code
    return send_sms(body, from_, to)
