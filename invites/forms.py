from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from core.forms import RightColumn
from core.models import User
from .models import InviteCode


class RegisterForm(UserCreationForm):
    code = forms.CharField(label=_("Code"))

    def clean_code(self):
        code = self.cleaned_data["code"]

        try:
            InviteCode.objects.get(code=code)
        except InviteCode.DoesNotExist:
            raise forms.ValidationError(_("Code is not valid!"))

        return code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("code"),
            Field("username"),
            Field("email"),
            Field("password1"),
            Field("password2"),
            RightColumn(Submit("submit", _("Register"))),
        )

        self.fields["email"].required = True

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]
