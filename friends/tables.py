from django.utils.translation import gettext_lazy as _
import django_tables2 as tables


class FriendsTable(tables.Table):
    from_user = tables.TemplateColumn(
        template_name="friends/includes/_column-friend.html", verbose_name=_("Friend")
    )
    actions = tables.TemplateColumn(
        template_name="friends/includes/_column-friend-actions.html",
        attrs={"cell": {"class": "w-[250px]"}},
        verbose_name=_("Actions"),
    )

    class Meta:
        orderable = False


class FriendSuggestionsTable(tables.Table):
    suggestion = tables.TemplateColumn(
        template_name="friends/includes/_column-suggestion.html",
        empty_values=(),
        verbose_name=_("Suggestion"),
    )
    actions = tables.TemplateColumn(
        template_name="friends/includes/_column-suggestion-actions.html",
        verbose_name=_("Actions"),
    )

    class Meta:
        orderable = False


class FriendRequestsTable(tables.Table):
    from_user = tables.TemplateColumn(
        template_name="friends/includes/_column-friend.html",
        extra_context={"show_created": True, "show_message": True},
        verbose_name=_("From"),
    )
    actions = tables.TemplateColumn(
        template_name="friends/includes/_column-friend-request-actions.html",
        attrs={"cell": {"class": "w-[250px]"}},
        verbose_name=_("Actions"),
    )

    class Meta:
        orderable = False


class FriendRequestsSentTable(tables.Table):
    to_user = tables.TemplateColumn(
        template_name="friends/includes/_column-friend.html",
        verbose_name=_("To"),
    )
    actions = tables.TemplateColumn(
        template_name="friends/includes/_column-friend-request-sent-actions.html",
        verbose_name=_("Actions"),
    )

    class Meta:
        orderable = False
