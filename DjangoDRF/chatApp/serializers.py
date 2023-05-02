from rest_framework import serializers
from .models import *
from api.address.serializers import ProfileSerializer,ProfilePicSerializer


class ChatMessageSerializer(serializers.ModelSerializer):
    '''
    This serializer is used to serialize the chat message details.
    '''
    user = ProfilePicSerializer(read_only=True)
    class Meta:
        '''
        This class is used to define the fields for the serializer.
        '''
        model = ChatMessage
        fields = ('id','user','message','created_at', 'updated_at')

class ThreadSerializer(serializers.ModelSerializer):
    '''
    This serializer is used to serialize the chat thread details.
    '''
    user_from = ProfileSerializer(read_only=True)
    user_to = ProfileSerializer(read_only=True)
    class Meta:
        '''
        This class is used to define the fields for the serializer.
        '''
        model = Thread
        fields = ('id','user_from','user_to','created_at', 'updated_at')
