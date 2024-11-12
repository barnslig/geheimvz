from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MessageOfTheDay(models.Model):
    class Meta:
        verbose_name = _("Message of the day")
        verbose_name_plural = _("Messages of the days")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Created by"),
    )

    message = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Message"),
    )

    def __str__(self):
        return self.message
