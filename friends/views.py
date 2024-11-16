from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from friendship.models import Friend, FriendshipRequest

from core.components.tabs.tabs import make_tabs
from core.models import User

from .forms import FriendAddForm
from .tables import (
    FriendRequestsSentTable,
    FriendRequestsTable,
    FriendSuggestionsTable,
    FriendsTable,
)
from .tasks import send_on_friend_request

tabs = {
    "list": {
        "href": reverse_lazy("friends"),
        "label": _("All friends"),
    },
    "suggestions": {
        "href": reverse_lazy("friend-suggestions"),
        "label": _("Find friends"),
    },
    "requests": {
        "href": reverse_lazy("friend-requests"),
        "label": _("Friend requests"),
    },
    "sent": {
        "href": reverse_lazy("friend-requests-sent"),
        "label": _("Sent friend requests"),
    },
}


@login_required
@ratelimit(key="user", rate="1/m", method="POST")
@ratelimit(key="user", rate="40/d", method="POST")
def friend_add(request: HttpRequest, pk: str):
    other_user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = FriendAddForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            Friend.objects.add_friend(request.user, other_user, message)

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Friendship request sent."),
            )

            if other_user.notification_settings.on_new_friend_request:
                send_on_friend_request.delay(
                    request.user.display_name,
                    other_user.display_name,
                    other_user.email,
                )

            return redirect(other_user)
    else:
        form = FriendAddForm()

    ctx = {
        "form": form,
        "other_user": other_user,
    }

    return render(request, "friends/friend_add.html", ctx)


@login_required
def friend_remove(request: HttpRequest, pk: str):
    other_user = get_object_or_404(User, pk=pk)

    if not Friend.objects.are_friends(request.user, other_user):
        raise Http404()

    if request.method == "POST":
        Friend.objects.remove_friend(request.user, other_user)

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Friendship ended."),
        )

        return redirect(other_user)

    ctx = {
        "headline": _("End friendship with %(name)s")
        % {"name": other_user.display_name},
        "copy": _("Are you sure that you want to end the friendship with %(name)s?")
        % {"name": other_user.display_name},
        "cancel_href": reverse_lazy("friends"),
    }

    return render(request, "core/confirmation.html", ctx)


@login_required
def friend_list(request: HttpRequest):
    current_tabs = make_tabs(tabs, "list")

    friends = (
        Friend.objects.select_related("from_user")
        .filter(to_user=request.user)
        .order_by("-created")
    )
    table = FriendsTable(friends)

    table.paginate(page=request.GET.get("page", 1), per_page=20)

    ctx = {
        "table": table,
        "tabs": current_tabs,
    }

    return render(request, "friends/friend_list.html", ctx)


@login_required
def friend_suggestions(request: HttpRequest):
    current_tabs = make_tabs(tabs, "suggestions")

    fof = request.user.get_friends_of_friends()
    table = FriendSuggestionsTable(fof)

    table.paginate(page=request.GET.get("page", 1), per_page=20)

    ctx = {
        "table": table,
        "tabs": current_tabs,
    }

    return render(request, "friends/friend_suggestions.html", ctx)


@login_required
def friend_requests(request: HttpRequest):
    current_tabs = make_tabs(tabs, "requests")

    friend_requests = (
        FriendshipRequest.objects.select_related("from_user", "to_user")
        .filter(to_user=request.user)
        .order_by("-created")
    )
    table = FriendRequestsTable(friend_requests)

    table.paginate(page=request.GET.get("page", 1), per_page=20)

    ctx = {
        "table": table,
        "tabs": current_tabs,
    }

    return render(request, "friends/friend_requests.html", ctx)


@login_required
def friend_requests_sent(request: HttpRequest):
    current_tabs = make_tabs(tabs, "sent")

    friend_requests_sent = Friend.objects.sent_requests(request.user)

    table = FriendRequestsSentTable(friend_requests_sent)

    ctx = {
        "table": table,
        "tabs": current_tabs,
    }

    return render(request, "friends/friend_requests_sent.html", ctx)


@login_required
def friendship_accept(request: HttpRequest, pk: int):
    if request.method == "POST":
        f_request = get_object_or_404(request.user.friendship_requests_received, id=pk)
        f_request.accept()
        return redirect("profile", id=f_request.to_user.id)

    return redirect("friend-requests")


@login_required
def friendship_reject(request: HttpRequest, pk: int):
    if request.method == "POST":
        f_request = get_object_or_404(request.user.friendship_requests_received, id=pk)
        f_request.cancel()
        return redirect("friend-requests")

    return redirect("friend-requests")


@login_required
def friendship_cancel(request: HttpRequest, pk: int):
    if request.method == "POST":
        f_request = get_object_or_404(request.user.friendship_requests_sent, id=pk)
        f_request.cancel()
        return redirect("friend-requests-sent")

    return redirect("friend-requests-sent")
