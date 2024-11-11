from django_components import Component, register
from django.utils.translation import gettext_lazy as _


@register("profile_image")
class ProfileImage(Component):
    template_name = "profile_image.html"

    def get_context_data(self, obj, image_field, alt=None):
        return {
            "alt": alt if alt else _("Profile picture"),
            "img": getattr(obj, image_field),
        }
