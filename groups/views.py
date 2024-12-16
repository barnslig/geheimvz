from django.urls import reverse_lazy
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from core.components.tabs.tabs import TabsMixin, make_tabs

from .models import ForumPost, ForumThread, Group, GroupInvitation
from .tables import GroupInviteTable, ThreadsTable
from .tasks import send_on_group_invitation
from .forms import (
    ForumPostForm,
    ForumThreadCreateForm,
    GroupCreateForm,
    GroupForm,
    GroupInviteForm,
)

User = get_user_model()

tabs = {
    "list": {
        "href": reverse_lazy("groups"),
        "label": _("My groups"),
    },
    "all": {
        "href": reverse_lazy("groups-all"),
        "label": _("Find groups"),
    },
    "invitations": {
        "href": reverse_lazy("group-invitations"),
        "label": _("Group invitations"),
    },
    "create": {
        "href": reverse_lazy("group-create"),
        "label": _("Create new group"),
    },
}


class GroupDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Group
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        latest_threads = self.object.threads.order_by("-updated_at")
        latest_threads_table = ThreadsTable(latest_threads)

        is_member = self.object.members.contains(self.request.user)
        is_invited = (
            not is_member
            and self.request.user.group_invitations_received.filter(
                for_group=self.object
            ).exists()
        )

        context = super().get_context_data(**kwargs)
        context["can_invite"] = self.object.get_can_invite(self.request.user)
        context["can_join"] = not self.object.is_private or is_invited
        context["is_admin"] = self.object.admins.contains(self.request.user)
        context["is_member"] = is_member
        context["is_invited"] = is_invited
        context["latest_threads_table"] = latest_threads_table
        return context


class GroupListView(TabsMixin, LoginRequiredMixin, ListView):
    model = Group
    paginate_by = 20
    ordering = ["name"]
    tabs = tabs
    tab_current = "list"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(members=self.request.user)


class GroupListAllView(TabsMixin, LoginRequiredMixin, ListView):
    model = Group
    paginate_by = 20
    template_name_suffix = "_list_all"
    ordering = ["name"]
    tabs = tabs
    tab_current = "all"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(members=self.request.user)


@method_decorator(ratelimit(key="user", rate="2/d", method="POST"), name="post")
class GroupCreateView(TabsMixin, LoginRequiredMixin, CreateView):
    form_class = GroupCreateForm
    model = Group
    success_message = _('Group "%(name)s" successfully created!')
    template_name_suffix = "_create"
    tabs = tabs
    tab_current = "create"

    def form_valid(self, form):
        self.object = form.save()

        self.object.created_by = self.request.user
        self.object.admins.add(self.request.user)
        self.object.members.add(self.request.user)

        return super().form_valid(form)


@method_decorator(ratelimit(key="user", rate="4/15m", method="POST"), name="post")
class GroupUpdateView(LoginRequiredMixin, UpdateView):
    form_class = GroupForm
    model = Group
    success_message = _('Group "%(name)s" successfully updated!')

    def get_queryset(self):
        return super().get_queryset().filter(admins__in=[self.request.user.pk])


@login_required
def group_leave(request: HttpRequest, pk: str):
    group = get_object_or_404(request.user.groups_member, pk=pk)

    if request.method == "POST":
        group.members.remove(request.user)
        group.admins.remove(request.user)

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Group successfully left"),
        )

        return redirect("group", pk=group.pk)

    ctx = {
        "headline": _('Leave group "%(name)s"?') % {"name": group.name},
        "copy": _('Do you want to leave the group "%(name)s"?') % {"name": group.name},
        "cancel_href": reverse_lazy("group", kwargs={"pk": group.pk}),
    }

    return render(request, "core/confirmation.html", ctx)


@login_required
def group_join(request: HttpRequest, pk: str):
    group = get_object_or_404(Group, pk=pk)

    try:
        invitation = request.user.group_invitations_received.get(for_group=group)
    except GroupInvitation.DoesNotExist:
        invitation = None

    if group.is_private and not invitation:
        raise PermissionDenied()

    if request.method == "POST":
        with transaction.atomic():
            group.members.add(request.user)

            if invitation:
                invitation.delete()

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Group successfully joined"),
        )

        return redirect("group", pk=group.pk)

    ctx = {
        "headline": _('Join group "%(name)s"?') % {"name": group.name},
        "copy": _('Do you want to join the group "%(name)s"?') % {"name": group.name},
        "cancel_href": reverse_lazy("group-invitations"),
    }

    return render(request, "core/confirmation.html", ctx)


@login_required
def group_invite(request: HttpRequest, pk: str):
    group = get_object_or_404(request.user.groups_member, pk=pk)

    to_user_queryset = User.objects.filter(friends__from_user=request.user).filter(
        ~Q(groups_member__pk=group.pk)
    )

    if request.method == "POST":
        invitation = GroupInvitation()
        invitation.from_user = request.user
        invitation.for_group = group

        form = GroupInviteForm(to_user_queryset, request.POST, instance=invitation)

        if form.is_valid():
            invitation = form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _("User successfully invited"),
            )

            if invitation.to_user.notification_settings.on_new_group_invitation:
                send_on_group_invitation.send(
                    invitation.from_user.display_name,
                    invitation.to_user.display_name,
                    invitation.for_group.name,
                    invitation.to_user.email,
                )

            return redirect("group", pk=group.pk)
    else:
        form = GroupInviteForm(to_user_queryset)

    ctx = {"group": group, "form": form}
    return render(request, "groups/group_invite.html", ctx)


@login_required
def group_invite_reject(request: HttpRequest, pk: str):
    invitation = get_object_or_404(request.user.group_invitations_received, pk=pk)
    invitation.delete()
    return redirect("group-invitations")


@login_required
def group_list_invites(request: HttpRequest):
    invitations = request.user.group_invitations_received.order_by("-created_at")
    table = GroupInviteTable(invitations)
    current_tabs = make_tabs(tabs, "invitations")
    ctx = {"table": table, "tabs": current_tabs}
    return render(request, "groups/group_list_invitations.html", ctx)


@login_required
def forumthread_list(request: HttpRequest, pk: str):
    group = get_object_or_404(request.user.groups_member, pk=pk)

    threads = group.threads.order_by("-updated_at")
    threads_table = ThreadsTable(threads)

    ctx = {"group": group, "table": threads_table}

    return render(request, "groups/forumthread_list.html", ctx)


@login_required
def forumthread_detail(request: HttpRequest, pk: str):
    thread = get_object_or_404(ForumThread, pk=pk)

    if not request.user.groups_member.contains(thread.group):
        raise PermissionDenied()

    posts = thread.posts.order_by("created_at")
    posts_paginator = Paginator(posts, 20)
    posts_page_obj = posts_paginator.get_page(request.GET.get("page", 1))

    ctx = {
        "thread": thread,
        "page_obj": posts_page_obj,
    }

    return render(request, "groups/forumthread_detail.html", ctx)


@ratelimit(key="user", rate="2/15m", method="POST")
@ratelimit(key="user", rate="6/d", method="POST")
@login_required
def forumthread_create(request: HttpRequest, pk: str):
    group = get_object_or_404(Group, pk=pk)

    if not group.get_can_create_thread(request.user):
        raise PermissionDenied()

    if request.method == "POST":
        form = ForumThreadCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                thread = ForumThread()
                thread.created_by = request.user
                thread.group = group
                thread.topic = form.cleaned_data["topic"]
                thread.save()

                post = ForumPost()
                post.created_by = request.user
                post.thread = thread
                post.post = form.cleaned_data["post"]
                post.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Thread successfully created"),
            )

            return redirect("forumthread_detail", pk=thread.pk)

    else:
        form = ForumThreadCreateForm()

    ctx = {
        "group": group,
        "form": form,
    }

    return render(request, "groups/forumthread_create.html", ctx)


@ratelimit(key="user", rate="10/15m", method="POST")
@ratelimit(key="user", rate="40/d", method="POST")
@login_required
def forumpost_create(request: HttpRequest, pk: str):
    thread = get_object_or_404(ForumThread, pk=pk)

    if not thread.get_can_create_post(request.user):
        raise PermissionDenied()

    if request.method == "POST":
        post = ForumPost()
        post.created_by = request.user
        post.thread = thread

        form = ForumPostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Post successfully created"),
            )

            return redirect("forumthread_detail", pk=thread.pk)
    else:
        form = ForumPostForm()

    ctx = {
        "group": thread.group,
        "thread": thread,
        "form": form,
    }

    return render(request, "groups/forumpost_create.html", ctx)


@login_required
def forumpost_attachment(request: HttpRequest, pk: str):
    post = get_object_or_404(ForumPost, pk=pk)

    if not request.user.groups_member.contains(post.thread.group):
        raise PermissionDenied()

    ctx = {"post": post, "thread": post.thread}

    return render(request, "groups/forumpost_attachment.html", ctx)
