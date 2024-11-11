from django_components import Component, register


@register("section")
class Section(Component):
    template_name = "section.html"

    def get_context_data(self, headline):
        return {
            "headline": headline,
        }
