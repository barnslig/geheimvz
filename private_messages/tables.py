from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import django_tables2 as tables

from .models import PrivateMessage


class BasePrivateMessageTable(tables.Table):
    subject = tables.Column(empty_values=())
    created_at = tables.Column(verbose_name=_("Sent at"))

    def render_subject(self, record, value):
        url = reverse("message_detail", kwargs={"pk": record.pk})

        label = "[" + _("No subject") + "]"
        if value:
            label = value

        return mark_safe(f'<a href="{url}">{label}</a>')


class PrivateMessagesTable(BasePrivateMessageTable):
    seen = tables.TemplateColumn(
        template_name="private_messages/includes/_column-seen.html",
        verbose_name="",
        attrs={"th": {"class": "w-0"}},
    )
    from_user = tables.Column(linkify=True)

    class Meta:
        model = PrivateMessage
        fields = ["seen", "from_user", "subject", "created_at"]
        orderable = False
        row_attrs = {"class": lambda record: "font-bold" if not record.seen else ""}


class PrivateMessagesSentTable(BasePrivateMessageTable):
    to_user = tables.Column(linkify=True)

    class Meta:
        model = PrivateMessage
        fields = ["to_user", "subject", "created_at"]
        orderable = False
