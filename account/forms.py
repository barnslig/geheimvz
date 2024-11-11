from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _, gettext

from core.models import User
from core.forms import RightColumn


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("username"),
            Field("email"),
            RightColumn(Submit("submit", _("save"))),
        )

        self.fields["email"].required = True


class AppearanceForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "appearance_color",
            "appearance_font",
            "appearance_size",
            "appearance_background",
            "appearance_logo",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("appearance_color"),
            Field("appearance_font"),
            Field("appearance_size"),
            Field("appearance_background"),
            Field("appearance_logo"),
            RightColumn(Submit("submit", _("save"))),
        )


class PrivacyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "can_see_profile",
            "can_send_messages",
        ]
        help_texts = {
            "can_see_profile": "Dein Profilbild und dein Name sind immer für alle zu sehen.",
            "can_send_messages": "Freunde und Leute, denen du eine Freundschaftsanfrage gesendet hast, dürfen dir immer schreiben.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("can_see_profile"),
            Field("can_send_messages"),
            RightColumn(Submit("submit", _("save"))),
        )


class DeleteForm(forms.Form):
    confirm = forms.CharField(label=_('Type "%s" to confirm.') % (_("yes, i want"),))

    def clean_confirm(self):
        confirm = self.cleaned_data["confirm"]

        if confirm != gettext("yes, i want"):
            raise forms.ValidationError(_("Not correct!"))

        return confirm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("confirm"),
            RightColumn(Submit("submit", _("Delete account"))),
        )


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("old_password"),
            Field("new_password1"),
            Field("new_password2"),
            RightColumn(Submit("submit", _("Change password"))),
        )


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_class = "mb-2"
        self.helper.label_class = "block text-base-accent"
        self.helper.layout = Layout(
            Field("username"),
            Field("password"),
            Submit("submit", _("Login")),
        )

        self.fields["username"].widget = forms.TextInput()  # disable autofocus
