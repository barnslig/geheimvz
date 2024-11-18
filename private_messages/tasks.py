import dramatiq

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


@dramatiq.actor
def send_on_receive_mail(from_name: str, to_name: str, to_email: str):
    ctx = {
        "from_name": from_name,
        "to_name": to_name,
        "action_url": settings.BASE_URL,
    }

    subject = f"Neue Nachricht!"
    message = render_to_string("private_messages/mails/on_receive.txt", ctx)

    send_mail(subject, message, None, [to_email])
