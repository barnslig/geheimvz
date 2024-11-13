from django_ratelimit.decorators import ratelimit
from django_tables2 import SingleTableView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from core.components.tabs.tabs import TabsMixin

from .forms import PrivateMessageForm
from .models import PrivateMessage
from .tables import PrivateMessagesSentTable, PrivateMessagesTable
from .tasks import send_on_receive_mail

User = get_user_model()

tabs = {
    "list": {
        "href": reverse_lazy("messages"),
        "label": _("Inbox"),
    },
    "sent": {
        "href": reverse_lazy("messages_sent"),
        "label": _("Sent"),
    },
    "create": {
        "href": reverse_lazy("message_create"),
        "label": _("New message"),
    },
}


class PrivateMessageListView(TabsMixin, LoginRequiredMixin, SingleTableView):
    model = PrivateMessage
    table_class = PrivateMessagesTable
    paginate_by = 5
    ordering = ["-created_at"]
    tabs = tabs
    tab_current = "list"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(to_user=self.request.user)


class PrivateMessageListSentView(TabsMixin, LoginRequiredMixin, SingleTableView):
    model = PrivateMessage
    table_class = PrivateMessagesSentTable
    paginate_by = 5
    ordering = ["-created_at"]
    template_name_suffix = "_list_sent"
    tabs = tabs
    tab_current = "sent"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(from_user=self.request.user)


class PrivateMessageDetailView(LoginRequiredMixin, DetailView):
    model = PrivateMessage

    def get(self, request: HttpRequest, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if self.object.to_user == request.user and not self.object.seen:
            self.object.seen = True
            self.object.save()

        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(to_user=self.request.user) | Q(from_user=self.request.user)
        )


@method_decorator(ratelimit(key="user", rate="1/m", method="POST"), name="post")
@method_decorator(ratelimit(key="user", rate="20/d", method="POST"), name="post")
class PrivateMessageCreateView(
    TabsMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = PrivateMessageForm
    model = PrivateMessage
    success_message = _("Private message successfully sent!")
    success_url = reverse_lazy("messages_sent")
    tabs = tabs
    tab_current = "create"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["from_user"] = self.request.user

        if "pk" in self.kwargs:
            friends = User.objects.filter(friends__from_user=self.request.user)
            kwargs["to_user"] = get_object_or_404(friends, pk=self.kwargs["pk"])

        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.from_user = self.request.user

        if self.object.to_user.notification_settings.on_new_private_message:
            send_on_receive_mail.delay(
                self.object.from_user.display_name,
                self.object.to_user.display_name,
                self.object.to_user.email,
            )

        return super().form_valid(form)
