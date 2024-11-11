from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from core.forms import RightColumn
from emoticons.forms import EmoticonPicker

from .models import PinboardMessage


class PinboardMessageForm(ModelForm):
    class Meta:
        model = PinboardMessage
        fields = ["message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("message"),
            EmoticonPicker("message"),
            RightColumn(Submit("submit", _("Write onto pinboard"))),
        )
