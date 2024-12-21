from django_prometheus.models import ExportModelOperationsMixin
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()


class PrivateMessage(ExportModelOperationsMixin("private_message"), models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)

    from_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="messages_sent",
        verbose_name=_("Sender"),
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_received",
        verbose_name=_("Recipient"),
    )

    subject = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Subject"),
    )
    message = models.TextField(verbose_name=_("Message"))
    seen = models.BooleanField(default=False, verbose_name=_("Seen"))

    def get_absolute_url(self):
        return reverse("message_detail", kwargs={"pk": self.pk})
