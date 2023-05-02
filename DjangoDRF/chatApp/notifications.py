from django.db.models import Q
import json
from firebase_admin.messaging import Message, Notification

from api.user.models import EmailUser, PhoneUser, SocialUser
from api.address.models import MyDevice, UserNotification, Profile
from api.chatapp.models import Thread, ChatMessage

def send_chat_notification(thread_id,sender_id,message):
    '''
    This function is used to send the chat notification to the user device.
    '''

    #get the thread details
    thread = Thread.objects.get(id=thread_id)
    if thread.user_from.user_id == int(sender_id):
        receiver = thread.user_to
        sender = thread.user_from
    else:
        receiver = thread.user_from
        sender = thread.user_to

    if sender.user_type == 'EMAIL':
        user = EmailUser.objects.get(id=sender.user_id)
        sender_name = '{} {}'.format(user.first_name, user.last_name)
    elif sender.user_type == 'PHONE':
        user = PhoneUser.objects.get(id=sender.user_id)
        sender_name = '{} {}'.format(user.first_name, user.last_name)
    else:
        user = SocialUser.objects.get(id=sender.user_id)
        sender_name = '{} {}'.format(user.first_name, user.last_name)

    #notification object 
    
    x = {
        "title": "New Message",
        "body": '{}: {}'.format(sender_name, message)
        "data": {
            "friend_id": str(sender.user_id),
            "friend_type": sender.user_type,
            "name": sender_name,
            "navigate"  : "chat",
        },
        "android": {
            "channelId": "default",
            "smallIcon": "ic_notification",
            "color": "#FFFFFF",
            "largeIcon": "ic_launcher",
            "pressAction": {
                "id": "chat",
                "launchActivity": "default"
            },
        }
    }

    data = json.dumps(x)

    try:
        device = MyDevice.objects.get(users_id=receiver.user_id, user_type=receiver.user_type)

        # Send the message to the device when the user send friend request
        if len(device.registration_id) > 0:
            device.send_message(Message(
            notification= Notification(
            title= "New Message",
            body = '{}: {}'.format(sender_name, message)
            ),
            data={"notifee":data}

            ))

        return True
    except MyDevice.DoesNotExist:
        return False
