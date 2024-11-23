from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class InviteCode(models.Model):
    class Meta:
        verbose_name = _("Invite code")
        verbose_name_plural = _("Invite codes")

    code = models.CharField(max_length=255, unique=True, verbose_name=_("Invite code"))
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="invite_codes",
        verbose_name=_("Owner"),
    )
    remaining = models.IntegerField(verbose_name=_("Remaining invites"))

    def __str__(self):
        return self.code
