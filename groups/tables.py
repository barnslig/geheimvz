from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.html import escape
from django.utils.safestring import mark_safe
import django_tables2 as tables

from core.components.actions.actions import Actions

from .models import ForumThread, GroupInvitation


class ThreadsTable(tables.Table):
    topic = tables.Column(linkify=True)
    posts = tables.Column(verbose_name=_("Posts"))
    updated_at = tables.Column(verbose_name=_("Last update"))

    def render_posts(self, record):
        return record.posts.count()

    def render_updated_at(self, record, value):
        template_name = "groups/includes/_column-last-update.html"
        ctx = {
            "updated_at": record.updated_at,
            "updated_by": record.posts.order_by("-created_at").all()[0].created_by,
        }
        return get_template(template_name).render(ctx)

    class Meta:
        model = ForumThread
        fields = ["topic", "updated_at"]
        sequence = ("topic", "posts", "updated_at")


class GroupInviteTable(tables.Table):
    invitation = tables.Column(empty_values=())
    actions = tables.Column(empty_values=())

    def render_invitation(self, record):

        return mark_safe(
            _(
                '<a href="%(from_url)s">%(from_name)s</a> invited you to group <a href="%(group_url)s">%(group_name)s</a>!'
            )
            % {
                "from_url": reverse_lazy("profile", kwargs={"id": record.from_user.pk}),
                "from_name": escape(record.from_user.display_name),
                "group_url": reverse_lazy("group", kwargs={"pk": record.for_group.pk}),
                "group_name": escape(record.for_group.name),
            }
        )

    def render_actions(self, record):
        return Actions.render(
            kwargs={
                "actions": [
                    {
                        "href": reverse_lazy(
                            "group-join",
                            kwargs={"pk": record.for_group.pk},
                        ),
                        "label": _("Accept invitation"),
                    },
                    {
                        "href": reverse_lazy(
                            "group-invite-reject",
                            kwargs={"pk": record.pk},
                        ),
                        "label": _("Reject invitation"),
                    },
                ]
            }
        )

    class Meta:
        model = GroupInvitation
        fields = []
