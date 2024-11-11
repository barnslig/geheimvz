from django_components import Component, register


@register("actions")
class Actions(Component):
    template_name = "actions.html"

    def get_context_data(self, actions):
        return {
            "actions": actions,
        }
