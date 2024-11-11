from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from core.forms import RightColumn
from emoticons.forms import EmoticonPicker

from .models import PrivateMessage

User = get_user_model()

Field.wrapper_class = "field"


class PrivateMessageForm(ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ["to_user", "subject", "message"]

    def __init__(self, from_user, to_user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["to_user"].queryset = User.objects.filter(
            friends__from_user=from_user
        )

        if to_user:
            self.fields["to_user"].disabled = True
            self.fields["to_user"].initial = to_user

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("to_user"),
            Field("subject"),
            Field("message"),
            EmoticonPicker("message"),
            RightColumn(
                Submit("submit", _("Send message")),
            ),
        )
