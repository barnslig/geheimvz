from django_components import Component, register
from django.utils.translation import gettext_lazy as _


@register("profile_image")
class ProfileImage(Component):
    template_name = "profile_image.html"

    def get_context_data(self, image_url, width, height, alt=None):
        return {
            "alt": alt if alt else _("Profile picture"),
            "img": image_url,
            "width": width,
            "height": height,
        }
