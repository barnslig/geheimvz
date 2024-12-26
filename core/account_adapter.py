from django.db import transaction
from django.utils.translation import gettext_lazy as _

from invites.models import InviteCode

from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)
        code = form.cleaned_data.get("code")

        with transaction.atomic():
            invite = InviteCode.objects.get(code=code)
            invite.remaining -= 1
            invite.save()

            if invite.owner:
                user.invited_by = invite.owner

            if commit:
                user.save()

        return user
