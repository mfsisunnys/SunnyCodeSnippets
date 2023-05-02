from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse

from .models import Evaluator, MemberShip, Section
from .sms import send_sms, send_otp_sms
from .email import send_email
from .utils import generate_otp, generate_random_password

import logging

logger = logging.getLogger(__name__)


def evalutor_list(request):
    '''
    This method is used to display all the evaluators
    '''
    all_evaluator = Evaluator.objects.all().order_by('-created_at')
    context = {
        'all_evaluator': all_evaluator,
    }
    return render(request, 'evalutor/evalutor_list.html', context)

def evalutor_add(request):
    '''
    This method is used to add new evaluator
    '''
    if request.method == 'POST':
        '''
        This method is used to add new evaluator
        '''
        if 'create' in request.POST:
            # create new evaluator
            membership_id = request.POST['membership']
            section = request.POST['section']
            add_evaluator = Evaluator(membership_id=membership_id, section_id=section, status=PAPER_STATUS['ACTIVE'])
            add_evaluator.save()
            # assign new role
            add_evaluator.membership.user.roles.clear()
            add_evaluator.membership.user.roles.add(Role.EVALUATOR)
            add_evaluator.membership.user.groups.clear()
            member_group = Group.objects.get(name__iexact='Evaluator')
            add_evaluator.membership.user.groups.add(member_group)
            
            email = [add_evaluator.membership.user.email]
            
            # send sms to user
            try:
                message = "you are invited as evaluator by {}".format(request.user)
                send_sms(message, add_evaluator.membership.user.profile.mobile_number)
            except Exception as e:
                logger.error('unable to send create sms to specific user')

            # send mail
            try:
                mailcontent = Mail.objects.get(name__iexact='EvaluatorAdd')
                mail_dict = {
                    'subject': mailcontent.email_subject,
                    'plain_message': mailcontent.email_body,
                    'html_message' : mailcontent.email_body,
                    'recipient_list': '{}'.format(add_evaluator.membership.user.email)
                }
                KosEmail.send_mail(**mail_dict)
            except Exception as e:
                logger.error('unable to send create mail to specific user')
                
            # send web socket notification to user
            message = "You added as evaluator by {} {}".format(request.user.first_name, request.user.last_name)
            WebNotification(request.user).send_only_notification_to_user([add_evaluator.membership.user], message)
            logger.info('evaluator added successfully')
            messages.success(request, 'Evaluator added successfully!')
            return HttpResponseRedirect(reverse('koscientific:evalutor_list'))

        if 'invite' in request.POST:
            # invite evaluator
            membership_id = request.POST['membership']
            section = request.POST['section']
            add_evaluator = Evaluator(membership_id=membership_id, section_id=section, status='InActive')
            add_evaluator.save()    
            email = [add_evaluator.membership.user.email, ]
            
            try:
                # send sms to member to become evaluator
                message = "you added as evaluator by {}".format(request.user)
                send_sms(message, add_evaluator.membership.user.profile.mobile_number)
                logger.info('evaluator invited successfully')
            except Exception as e:
                logger.error('unable to send invite sms to specific user')

            try:
                oneTimeLink = OneTimeLink()
                oneTimeLink.name = "evaluator add link"
                oneTimeLink.token = id_generator(50)
                oneTimeLink.save()
                
                kwargs = {
                    "uidb64": urlsafe_base64_encode(force_bytes(add_evaluator.membership.user.pk)),
                    "evaluator_id": urlsafe_base64_encode(force_bytes(add_evaluator.pk)),
                    "token": oneTimeLink.token 
                }
                
                confirm_url = reverse("koscientific:confirm_evaluator",  kwargs=kwargs)

                confirm_url = "{0}://{1}{2}".format(request.scheme, request.get_host(), confirm_url)

                # send mail to member to become evaluator
                mailcontent = Mail.objects.get(name__iexact='EvaluatorInvite')
                user_full_name = '{} {}'.format(add_evaluator.membership.user.first_name, add_evaluator.membership.user.last_name)
                mailcontent.email_body = mailcontent.email_body.replace('{{user}}', user_full_name)
                url = "<a href={}>{}</a>".format(confirm_url, confirm_url)
                mailcontent.email_body = mailcontent.email_body.replace('{{link}}', url)
                mail_dict = {
                    'subject': mailcontent.email_subject,
                    'plain_message': mailcontent.email_body,
                    'html_message' : mailcontent.email_body,
                    'recipient_list': '{}'.format(add_evaluator.membership.user.email)
                }
                KosEmail.send_mail(**mail_dict)
            except Exception as e:
                logger.error('unable to send invite mail to specific user')
                
            # web socket notification
            message = "Your invited as evaluated by {} {}".format(request.user.first_name, request.user.last_name)
            WebNotification(request.user).send_only_notification_to_user([add_evaluator.membership.user], message)
            
            messages.success(request, 'Evaluator invited successfully!')
            logger.info('evaluator invited successfully')
            return HttpResponseRedirect(reverse('koscientific:evalutor_list'))

    section_list = Section.objects.filter(status=PAPER_STATUS['ACTIVE'])

    # get all member who is not evaluator
    member_list = MemberShip.objects.filter(evaluator__membership__isnull=True, is_member=True)
    context = {
        'section_list': section_list,
        'member_list': member_list,
    }
    return render(request, 'evalutor/evalutor_add.html', context)

def confirm_evaluator(request,uidb64=None, evaluator_id=None, token=None):
    '''
    confirm evaluator
    '''
    if OneTimeLink.objects.filter(token = token).exists() and not is_token_expired(token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return HttpResponse(status=404, content="User does not exist")
        
        try:
            evaluator_id = force_text(urlsafe_base64_decode(evaluator_id))
            evaluator = Evaluator.objects.get(pk=evaluator_id)
            evaluator.status = PAPER_STATUS['ACTIVE']
            evaluator.save()
        except Evaluator.DoesNotExist:
            logger.error('evaluator does not exist')
            return HttpResponse(status=404, content="Evaluator does not exist")
        # assign new role
        user.roles.clear()
        user.roles.add(Role.EVALUATOR)
        user.groups.clear()
        member_group = Group.objects.get(name__iexact='Evaluator')
        user.groups.add(member_group)
        OneTimeLink.objects.filter(token = token).delete()
        messages.success(request, 'Congratulations now you are Evaluator')
        return redirect('koscientific:home')
    else:
        logger.error('link expired')
        return HttpResponse(status=400, content="Link expired")

def evaluator_edit(request, evaluator_id):
    '''
    edit evaluator
    '''
    eval_edit = Evaluator.objects.get(id=evaluator_id)
    if request.method == 'POST':
        if 'membership' in request.POST:
            eval_edit.membership_id = request.POST['membership']

        if 'section' in request.POST:
            eval_edit.section_id = request.POST['section']

        eval_edit.save()
        messages.success(request, 'Evaluator updated successfully!')
        return HttpResponseRedirect(reverse('koscientific:evaluter_list'))
    # pure members
    members = MemberShip.objects.filter(evaluator__membership__isnull =True, is_member=True)
    members = chain(members , Evaluator.objects.filter(id=evaluator_id))
    section_list = Section.objects.all()
    context = {
        'section_list': section_list,
        'eval_edit': eval_edit,
        'members': members,
    }
    logger.info('evaluator updated successfully')
    return render(request, 'evalutor/evalutor_edit.html', context)

    
