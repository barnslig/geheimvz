from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()


class PinboardMessage(models.Model):
    class Meta:
        verbose_name = _("Pinboard Message")
        verbose_name_plural = _("Pinboard Messages")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name=_("Created by")
    )
    created_for = models.ForeignKey(
        User,
        related_name="pinboard",
        on_delete=models.CASCADE,
        verbose_name=_("Created for"),
    )

    message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Pinboard Message"),
    )

    def get_can_delete_post(self, user):
        if self.created_for == user:
            return True

        if self.created_by == user:
            return True

        if user.is_superuser:
            return True

        return False
