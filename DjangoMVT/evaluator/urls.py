from django.urls import path
from .views import evalutor_add, evalutor_list, Evaluator_edit, confirm_evaluator

app_name='koscientific'

urlpatterns = [
    '''
    display all the urls here
    '''
    path('evalutor/add/',evalutor_add, name='evalutor_add'),
    path('evalutor/list/',evalutor_list, name='evalutor_list'),
    path('evalutor/edit/<int:evaluator_id>/',Evaluator_edit, name='evaluator_edit'),
    path('evaluator_confirm/<uidb64>/<evaluator_id>/<token>/', confirm_evaluator, name='confirm_evaluator'),
]