from django.contrib import admin
from django.urls import path
from .views import getchat, thread, openchats

urlpatterns = [
    '''
    display all the urls here like below
    '''
    path('chat/', getchat, name='getchat'),
    path('thread/', thread, name='thread'),

]
