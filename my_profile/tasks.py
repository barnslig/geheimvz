import dramatiq

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from core.models import User


@dramatiq.actor
def send_on_greeting_mail(from_id: str, to_id: str):
    from_user = User.objects.get(pk=from_id)
    to_user = User.objects.get(pk=to_id)

    ctx = {
        "from_user": from_user,
        "to_user": to_user,
        "action_url": settings.BASE_URL,
    }

    subject = from_user.profile.greeting_i18n["subject"]
    message = render_to_string("my_profile/mails/on_greeting.txt", ctx)

    send_mail(subject, message, None, [to_user.email])
