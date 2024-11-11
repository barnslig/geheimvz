from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms import RightColumn


class SearchForm(forms.Form):
    q = forms.CharField(label=_("Search query"), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            Field("q"),
            RightColumn(Submit("", _("Search"))),
        )
