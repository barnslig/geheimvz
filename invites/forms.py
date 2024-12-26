from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
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
