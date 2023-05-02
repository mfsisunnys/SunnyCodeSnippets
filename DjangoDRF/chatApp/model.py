from django.db import models

from api.address.models import Profile

class Thread(models.Model):
    '''
    This model is used to store the chat thread details.
    '''
    user_from = models.ForeignKey(Profile, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(Profile, related_name='user_to', on_delete=models.CASCADE)
    is_opened_from = models.BooleanField(default=False)
    is_opened_to = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        This method is used to return the string representation of the model to show in the admin panel.
        '''
        return '{}-{}'.format(self.user_from.user_id, self.user_to.user_id)

class ChatMessage(models.Model):
    '''
    This model is used to store the chat message details.
    '''
    thread = models.ForeignKey(Thread, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''
        This method is used to return the string representation of the model to show in the admin panel.
        '''
        return '{}-{}'.format(self.thread.id, self.user.user_id)
