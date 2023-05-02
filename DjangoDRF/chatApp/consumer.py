import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import logging

from .models import ChatMessage, Thread
from api.address.models import Profile
from api.chatapp.serializers import ChatMessageSerializer
from .notifications import send_chat_notification

logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    '''
    This class is used to handle the chat functionality
    '''
    def connect(self):
        '''
        This method is used to connect the websocket
        '''
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        try:
            thread = Thread.objects.get(id=self.thread_id)
            #find thread and open it
            if thread.user_from.user_id == int(self.user_id):
                thread.is_opened_from = True
                thread.save()
            elif thread.user_to.user_id == int(self.user_id):
                thread.is_opened_to = True
                thread.save()
            else :
                pass
        

            async_to_sync(self.channel_layer.group_add)(
                self.thread_id,
                self.channel_name
            )
            self.accept()
        
        except Exception as error:
            logger.error(error)
            return Response({ 'success':False, 'detail':'Unable to get connect ws. Please contact support' }, status=HTTP_500_INTERNAL_SERVER_ERROR)


    def disconnect(self, close_code):
        '''
        This method is used to disconnect the websocket
        '''
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        try:
            thread = Thread.objects.get(id=self.thread_id)
            if thread.user_from.user_id == int(self.user_id):
                thread.is_opened_from = False
            elif thread.user_to.user_id == int(self.user_id):
                thread.is_opened_to = False
            thread.save()
        except Exception as error:
            logger.error(error)
            return Response({ 'success':False, 'detail':'Unable to get connect ws. Please contact support' }, status=HTTP_500_INTERNAL_SERVER_ERROR)


    def receive(self, text_data):
        '''
        This method is used to receive the message
        '''
        text_data_json = json.loads(text_data)
        message = text_data_json['msg_info']
        site_url = settings.SITE_URL

        serializer_class = ChatMessageSerializer

        thread_id = self.scope['url_route']['kwargs']['thread_id']
        sender_id = self.scope['url_route']['kwargs']['user_id']

        try:

            thread = Thread.objects.get(id=thread_id)

            if int(sender_id) == thread.user_from.user_id:
                sender = thread.user_from
            else:
                sender = thread.user_to

            new_message = ChatMessage.objects.create(thread=thread, user=sender, message=message, is_read=True)
            new_message.save()
            serializer = serializer_class(new_message, many=False)

            # check if user is online, if not send notification
            if thread.user_from.id == sender.id:
                if thread.is_opened_to == False:
                    r = requests.get(site_url+'meeting/notification/'+str(thread_id)+'/'+str(sender_id)+'/'+str(message))
                    new_message.is_read = False
                    new_message.save()
            else:
                if thread.is_opened_from == False:
                    r = requests.get(site_url+'/meeting/notification/'+str(thread_id)+'/'+str(sender_id)+'/'+str(message))
                    new_message.is_read = False
                    new_message.save()


            async_to_sync(self.channel_layer.group_send)(
                self.thread_id,
                {
                    'type': 'chat_message',
                    'msg_info': serializer.data
                }
            )
        except Exception as error:
            logger.error(error)
            return Response({ 'success':False, 'detail':'Unable to send message. Please contact support' }, status=HTTP_500_INTERNAL_SERVER_ERROR)


    def chat_message(self, event):
        '''
        This method is used to send the message
        '''
        message = event['msg_info']
        try:
            self.send(text_data=json.dumps({
                'msg_info': message
            }))
        except Exception as error:
            logger.error(error)
            return Response({ 'success':False, 'detail':'Unable to send message. Please contact support' }, status=HTTP_500_INTERNAL_SERVER_ERROR)
