from django_components import Component, register


@register("list")
class List(Component):
    template_name = "list.html"
