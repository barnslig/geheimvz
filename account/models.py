from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class NotificationSettings(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )

    on_new_pinboard_message = models.BooleanField(
        default=True,
        verbose_name=_("On new pinboard message"),
    )
    on_new_private_message = models.BooleanField(
        default=True,
        verbose_name=_("On new private message"),
    )
    on_new_friend_request = models.BooleanField(
        default=True,
        verbose_name=_("On new friend request"),
    )
    on_new_group_invitation = models.BooleanField(
        default=True,
        verbose_name=_("On new group invitation"),
    )

    def __str__(self):
        return f"Settings for {self.owner.display_name}"
