from crispy_forms.layout import LayoutObject
from crispy_forms.utils import TEMPLATE_PACK
from django.template.loader import render_to_string

from .emoticons import emoticons


class EmoticonPicker(LayoutObject):
    template = "forms/layout/emoticon_picker.html"

    def __init__(self, for_field):
        self.for_field = for_field

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)

        ctx = {
            "obj": self,
            "for_field_id": form[self.for_field].auto_id,
            "form": form,
            "emoticons": emoticons,
        }

        return render_to_string(template, ctx)
