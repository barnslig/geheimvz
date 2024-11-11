from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, LayoutObject
from crispy_forms.utils import TEMPLATE_PACK
from crispy_tailwind.tailwind import CSSContainer
from crispy_tailwind.templatetags.tailwind_field import CrispyTailwindFieldNode
from django import forms
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string

from .models import User

Field.template = "forms/layout/field.html"
Fieldset.template = "forms/layout/fieldset.html"

base_input = "block w-full px-1 leading-normal border appearance-none text-base-content bg-base-100 border-secondary-300 focus:outline-none"

default_styles = {
    "text": base_input,
    "number": base_input,
    "radioselect": "",
    "email": base_input,
    "url": base_input,
    "password": base_input,
    "hidden": "",
    "multiplehidden": "",
    "file": "",
    "clearablefile": "",
    "textarea": base_input,
    "date": base_input,
    "datetime": base_input,
    "time": base_input,
    "checkbox": "",
    "select": base_input,
    "nullbooleanselect": "",
    "selectmultiple": "",
    "checkboxselectmultiple": "",
    "multi": "",
    "splitdatetime": "text-gray-700 bg-white focus:outline border border-gray-300 leading-normal px-4 "
    "appearance-none rounded-lg py-2 focus:outline-none mr-2",
    "splithiddendatetime": "",
    "selectdate": "",
    "error_border": "border-red-500",
}

default_css_container = CSSContainer(default_styles)
CrispyTailwindFieldNode.default_container = default_css_container


class RightColumn(LayoutObject):
    template = "forms/layout/right-column.html"

    def __init__(self, *fields):
        self.fields = list(fields)

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(form, context, template_pack, **kwargs)
        template = self.get_template_name(template_pack)
        return render_to_string(template, {"fields": fields})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "image",
            "full_name",
            "nickname",
            "pronouns",
            "birthday",
            "mothers_maiden_name",
            "name_of_first_pet",
            "grew_up_street",
            "first_car_make",
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
            Fieldset(
                _("Profile picture"),
                Field("image"),
            ),
            Fieldset(
                _("General"),
                Field("full_name"),
                Field("nickname"),
                Field("pronouns"),
                Field("birthday"),
            ),
            Fieldset(
                _("Personal"),
                Field("mothers_maiden_name"),
                Field("name_of_first_pet"),
                Field("grew_up_street"),
                Field("first_car_make"),
                Field("relationship"),
                Field("looking_for"),
                Field("hobbies"),
                Field("what_i_like"),
                Field("what_i_dont_like"),
                Field("favourite_music"),
                Field("favourite_movies"),
                Field("favourite_books"),
                Field("favourite_food"),
                Field("i_am_good_at"),
                Field("i_wish_for"),
            ),
            RightColumn(Submit("submit", _("save"))),
        )
