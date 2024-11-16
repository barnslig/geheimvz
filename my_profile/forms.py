from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from core.forms import RightColumn

from .models import MyProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyProfile
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
