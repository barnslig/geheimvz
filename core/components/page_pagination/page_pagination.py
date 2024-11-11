from django_components import Component, register


@register("page_pagination")
class PagePagination(Component):
    template_name = "page_pagination.html"

    def get_context_data(self, page_obj):
        return {
            "page_obj": page_obj,
        }
