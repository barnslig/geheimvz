from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path(
        "hilfe.php",
        TemplateView.as_view(template_name="static_pages/help.html"),
        name="static_help",
    ),
    path(
        "privacy.php",
        TemplateView.as_view(template_name="static_pages/privacy.html"),
        name="static_privacy",
    ),
    path(
        "rules.php",
        TemplateView.as_view(template_name="static_pages/rules.html"),
        name="static_rules",
    ),
]
