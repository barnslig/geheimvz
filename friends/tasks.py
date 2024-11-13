from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


@shared_task
def send_on_friend_request(from_name: str, to_name: str, to_email: str):
    ctx = {
        "from_name": from_name,
        "to_name": to_name,
        "action_url": settings.BASE_URL,
    }

    subject = f"Neue Freunde!"
    message = render_to_string("friends/mails/on_friend_request.txt", ctx)

    send_mail(subject, message, None, [to_email])
