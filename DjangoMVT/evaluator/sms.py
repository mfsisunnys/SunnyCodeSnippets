import http.client as http_client
import json
from django.conf import settings
import requests

from kosscientific.settings import sms_credential


def send_sms(message, mobile_number):
    """ send sms to given number """
    if settings.CAN_SEND_SMS:
        if not mobile_number:
            raise Exception('mobile number required')

        
        api = sms_credential.get('api')
        auth_key = sms_credential.get('auth_key')
        mobile_number = mobile_number
        message = message
        sender = sms_credential.get('sender')
        route = sms_credential.get('route')
        country = sms_credential.get('country')
        final_sms_api_format = '{}?authkey={}&mobiles={}&message={}&sender={}&route={}&country={}'.format(
            api, auth_key, mobile_number, message, sender, route, country
        )

        try:
            sms_response = requests.get(final_sms_api_format)
            return 'success', sms_response
        except Exception as e:
            return 'error', None
    else:
        raise Exception('sms function is disabled by admin')


def send_otp_sms(message, mobile_number, otp):
    """ send otp sms"""
    if settings.CAN_SEND_SMS:
        if not mobile_number:
            raise Exception('mobile number required')
        country = sms_credential.get('country')
        api = sms_credential.get('otp_api')
        auth_key = sms_credential.get('auth_key')
        mobile_number = str(country) + str(mobile_number)
        message = message
        sender = sms_credential.get('sender')
        otp_expiry = sms_credential.get('otp_expiry')

        final_otp_sms_api_format = '{}?authkey={}&mobiles={}&message={}&sender={}&otp={}&otp_expiry={}'.format(
            api, auth_key, int(mobile_number), message, sender, otp, otp_expiry
        )

        try:
            sms_response = requests.get(final_otp_sms_api_format)
            return 'success', json.loads(sms_response.text)
        except Exception as e:
            return 'error', None
    else:
        raise Exception('sms function is disabled by admin')


