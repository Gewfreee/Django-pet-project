from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from library.models import User


@shared_task
def send_reset_code_email(user_id, reset_code):
    user = User.objects.get(pk=user_id)
    html_message = render_to_string('reset_email.html',
                                    {'username' : user.username, 'code' : reset_code})
    plain_message = strip_tags(html_message)

    send_mail(
        subject="Password reset",
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,)