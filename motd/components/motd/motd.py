from django_components import Component, register

from motd.models import MessageOfTheDay


@register("motd")
class Motd(Component):
    template_name = "motd.html"

    def get_context_data(self):
        message = MessageOfTheDay.objects.order_by("-created_at").first()
        return {
            "message": message,
        }
