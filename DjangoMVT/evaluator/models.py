from django.db import models
from datetime import datetime
from cities_light.models import City, Country,Region
from ckeditor.fields import RichTextField

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.translation import ugettext_lazy as _


class Role(models.Model):
    '''
    This model is used to store the role of the user.
    '''
    ADMIN = 1
    EVALUATOR = 2
    MEMBER = 3
    REGISTERED = 4
    ATTENDEE = 5

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (EVALUATOR, 'Evaluator'),
        (MEMBER, 'Member'),
        (REGISTERED, 'Registered'),
        (ATTENDEE,'Attendee'),

    )
    id = models.PositiveSmallIntegerField(('select role'), choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        '''
        This method is used to return the role id in django admin panel.
        '''
        return str(self.id)


class Evaluator(models.Model):
    '''
    This model is used to store the evaluator details.
    '''
    membership = models.ForeignKey(MemberShip, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(Section,on_delete=models.SET_NULL,blank=True,null=True)
    count=models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=25, blank=True, null=True)
    is_previous = models.BooleanField(_("is it last evaluator"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    __str__(self):
        '''
        This method is used to return the evaluator id in django admin panel.
        '''
        return str(self.id)

