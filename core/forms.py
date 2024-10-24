from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, LayoutObject
from crispy_forms.utils import TEMPLATE_PACK
from django.forms import ModelForm
from django.utils.translation import gettext as _
from django.template.loader import render_to_string

from .models import User

Fieldset.template = "forms/layout/fieldset.html"


class Section(LayoutObject):
    template = "forms/layout/section.html"

    def __init__(self, headline, *fields):
        self.headline = headline
        self.fields = list(fields)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, context, template_pack, **kwargs)

        template = self.get_template_name(template_pack)
        return render_to_string(template, {"section": self, "fields": fields})


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "image",
            "nickname",
            "pronouns",
            "birthday",
            "looking_for",
            "relationship",
            "hobbies",
            "what_i_like",
            "what_i_dont_like",
            "favourite_music",
            "favourite_movies",
            "favourite_books",
            "favourite_food",
            "i_am_good_at",
            "i_wish_for",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Section(_("Profile picture"), "image"),
            Section(
                _("Informations"),
                Fieldset(_("General"), "nickname", "pronouns", "birthday"),
                Fieldset(
                    _("Personal"),
                    "looking_for",
                    "relationship",
                    "hobbies",
                    "what_i_like",
                    "what_i_dont_like",
                    "favourite_music",
                    "favourite_movies",
                    "favourite_books",
                    "favourite_food",
                    "i_am_good_at",
                    "i_wish_for",
                ),
            ),
            Submit("submit", _("save")),
        )
