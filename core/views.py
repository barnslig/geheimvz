from csp.decorators import csp_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import cache_page
from friendship.models import Friend

from groups.models import Group
from private_messages.models import PrivateMessage


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("index-login")

    return render(request, "core/index.html", {})


@login_required
def index_login(request: HttpRequest):
    ctx = {}
    ctx["friend_requests"] = Friend.objects.unrejected_request_count(request.user)
    ctx["unread_messages"] = (
        PrivateMessage.objects.filter(to_user=request.user).filter(seen=False).count()
    )
    ctx["group_invites"] = request.user.group_invitations_received.count()
    ctx["friend_suggestions"] = request.user.get_friends_of_friends()[:4]
    ctx["popular_groups"] = Group.objects.popular(request.user)[:5]
    return render(request, "core/index_login.html", ctx)


@cache_page(60 * 15)
def ratelimited_error(request: HttpRequest, exception):
    return render(request, "core/ratelimited.html", status=429)


@csp_exempt
def info(request: HttpRequest):
    param = request.GET.get("")

    if param == "PHPE9568F34-D428-11d2-A769-00AA001ACF42":
        return redirect(
            staticfiles_storage.url("core/PHPE9568F34-D428-11d2-A769-00AA001ACF42.gif")
        )
    elif param == "PHPE9568F35-D428-11d2-A769-00AA001ACF42":
        return redirect(
            staticfiles_storage.url("core/PHPE9568F35-D428-11d2-A769-00AA001ACF42.gif")
        )

    return render(
        request,
        "core/info.html",
        {"credits": param == "PHPB8B5F2A0-3C92-11d3-A3A9-4C7B08C10000"},
    )
