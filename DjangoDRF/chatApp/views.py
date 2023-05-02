from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render
from decouple import config
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
import logging

from api.address.models import Profile
from .serializers import ChatMessageSerializer
from .models import ChatMessage, Thread
from .pagination import MyPagination
from api.user.authentication import JWTAuthentication

logger = logging.getLogger(__name__)
paginator = MyPagination()

PROFILE_PICTURE_URL = config('PROFILE_PICTURE_URL')

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
def getchat(request):
    if request.method == 'GET':
        '''
        Get chat messages
        '''
        serializer_class = ChatMessageSerializer
        data = request.query_params

        try:
            user_from = Profile.objects.get(user_id=data.get('user_id'), user_type=data.get('user_type'))
            user_to = Profile.objects.get(user_id=data.get('friend_id'), user_type=data.get('friend_type'))
            
            thread = Thread.objects.get(Q(user_from=user_from, user_to=user_to) | Q(user_from=user_to, user_to=user_from))
            chat_messages = ChatMessage.objects.filter(thread=thread).order_by('-created_at')
            for each in chat_messages:
                each.is_read = True
                each.save()

            page = paginator.paginate_queryset(chat_messages, request)
            serializer = serializer_class(page, many=True)
            chat_messages = paginator.get_paginated_response(serializer.data)
            return Response({ 'success':True, 'detail':chat_messages.data }, status=HTTP_200_OK)

        except Exception as error:
            logger.error(error)
            return Response({ 'success':False, 'detail':'Unable to getchat. Please contact support' }, status=HTTP_500_INTERNAL_SERVER_ERROR)
           
@api_view(['GET','POST'])
@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
def thread(request):
    if request.method == 'GET':
        '''
        Get thread
        '''
        data = request.query_params
        serializer_class = ThreadSerializer
        try:
            thread = Thread.objects.get(id=data.get('id'))
            serializer = serializer_class(thread)
            return Response(status=HTTP_200_OK, data={'success':True, 'detail': serializer.data})
        except Exception as error:
            logger.error(error)
            return Response({ 'success':False, 'detail':'Unable to get thread. Please contact support' }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        '''
        Create thread
        '''
        data = request.data
        try:
            user_from = Profile.objects.get(user_id=data.get('user_id'), user_type=data.get('user_type'))
            user_to = Profile.objects.get(user_id=data.get('friend_id'), user_type=data.get('friend_type'))
            #get or create thread
            thread = Thread.objects.filter(Q(user_from=user_from, user_to=user_to) | Q(user_from=user_to, user_to=user_from))
            if thread.exists():
                thread = thread.first()
                return Response(status=HTTP_200_OK, data={'success':True, 'detail': {'thread': thread.id}})
            else:
                thread = Thread.objects.create(user_from=user_from, user_to=user_to)
                return Response(status=HTTP_200_OK, data={'success':True, 'detail': {'thread': thread.id}})
        except Exception as error:
            logger.error(error)
            return Response({ 'success':False, 'detail':'Unable to create thread. Please contact support' }, status=HTTP_500_INTERNAL_SERVER_ERROR)


