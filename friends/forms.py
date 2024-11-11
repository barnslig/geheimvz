from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy as _

from core.forms import RightColumn
from emoticons.forms import EmoticonPicker


class FriendAddForm(Form):
    message = forms.CharField(label=_("Your message"), widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("message"),
            EmoticonPicker("message"),
            RightColumn(Submit("submit", _("Send a friend request"))),
        )
