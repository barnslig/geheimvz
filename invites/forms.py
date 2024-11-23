from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .models import InviteCode


class SignupForm(AllauthSignupForm):
    field_order = ["code"]

    code = forms.CharField(label=_("Invite code"))

    def clean_code(self):
        code = self.cleaned_data["code"]

        try:
            invite = InviteCode.objects.get(code=code)
            if invite.remaining < 1:
                raise forms.ValidationError(_("Invite code is not valid!"))
        except InviteCode.DoesNotExist:
            raise forms.ValidationError(_("Invite code is not valid!"))

        return code

    def save(self, request):
        code = self.cleaned_data.get("code")

        with transaction.atomic():
            invite = InviteCode.objects.get(code=code)
            invite.remaining -= 1
            invite.save()

            user = super(SignupForm, self).save(request)

        return user
