import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from core.models import User


class UserTable(tables.Table):
    image = tables.TemplateColumn(
        template_name="search/includes/_column-image.html", empty_values=()
    )
    display_name = tables.Column(verbose_name=_("Name"), linkify=True)

    class Meta:
        model = User
        fields = ["image", "display_name"]
