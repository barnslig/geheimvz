from django_components import Component, register
import copy


@register("tabs")
class Tabs(Component):
    template_name = "tabs.html"

    def get_context_data(self, tabs):
        return {
            "tabs": tabs,
        }


def make_tabs(tabs, current_tab):
    current_tabs = copy.deepcopy(tabs)
    current_tabs[current_tab]["current"] = True
    return list(current_tabs.values())


class TabsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tabs"] = make_tabs(self.get_tabs(), self.get_current_tab())
        return context

    def get_tabs(self):
        return self.tabs

    def get_current_tab(self):
        return self.tab_current
