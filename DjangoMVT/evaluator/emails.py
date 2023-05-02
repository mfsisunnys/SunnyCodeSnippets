from django.core.mail import get_connection, send_mail as django_send_mail
from django.conf import settings

from koscientific.models import *


class KosEmail:

    @staticmethod
    def send_mail(**kwargs):
        '''
        This method is used to send mail
        '''
        if settings.CAN_SEND_MAIL:
            # get email settings from database
            email = MailSettings.objects.first()
            email_server = email.mail_server
            email_port = email.mail_port
            email_username = email.username
            email_password = email.password
            email_ssl = email.use_ssl

            # get connection
            connection = get_connection(host=email_server, port=email_port, username=email_username,
                                        password=email_password, use_tls=email_ssl)
            subject = kwargs['subject']
            plain_message = kwargs['plain_message']

            # get recipient list whom to send mail
            recipient_list = (kwargs['recipient_list']).split(',')
            html_message = kwargs.get('html_message', None)

            # send mail here using django send_mail function
            send = django_send_mail(subject=subject, message=plain_message, from_email=email_username,
                                    recipient_list=recipient_list, connection=connection, fail_silently=False,
                                    html_message=html_message)

            return 'success'
        else:
            raise Exception('Email function is disabled by admin')