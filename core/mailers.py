from django.core.mail import send_mail, send_mass_mail
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core import mail


def send_verification_mail(token, to, username, cc=[]):
    subject = 'Verify your mail'
    context = {
        "client": settings.CLIENT_URL,
        "title": subject,
        "sec_token": token,
        "username": username
    }

    mailer = Mailer()
    msg = mailer.generate_html_mail(
        subject, 'authentication/verify.html', context=context, to=(to,), cc=cc)
    return mailer.send_mail(msg)


class Mailer():

    def __init__(self):
        pass

    def __del__(self):
        print('destructor called')

    def send_mail(self, mail):
        return mail.send()

    def send_bulk_mail(self, mails):
        connection = mail.get_connection(fail_silently=False)
        connection.open()
        result = self.connection.send_messages(mails)
        connection.close()

        return result

    def generate_mail(self, subject, body, sender=settings.DEFAULT_FROM_EMAIL, to=[], subtype='text'):
        mail = EmailMessage(
            subject=subject,
            body=body,
            from_email=sender,
            to=to
        )

        mail.content_subtype = subtype
        return mail

    def generate_html_mail(self, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL, to=[], cc=[]):
        msg_html = render_to_string(template_name, context)
        msg = EmailMessage(subject=subject, body=msg_html,
                           from_email=sender, to=to, bcc=cc)
        msg.content_subtype = 'html'

        return msg
