from csp.decorators import csp_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView
from friendship.models import Friend

from groups.models import Group
from private_messages.models import PrivateMessage

from .forms import ProfileForm
from .models import User


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


@login_required
def profile(request: HttpRequest, id: str):
    user = get_object_or_404(User, id=id)

    def is_empty(x):
        if isinstance(x, str):
            return len(x.strip()) == 0
        return not x

    def make_section(headline, fields):
        section = {"headline": headline, "fields": []}
        for field in fields:
            label = user._meta.get_field(field).verbose_name
            value = getattr(user, field)
            if not is_empty(value):
                section["fields"].append({"label": label, "value": value})

        if len(section["fields"]) > 0:
            return section

        return None

    can_see_profile = user.privacy_settings.get_can_see_profile(request.user)
    can_send_messages = user.privacy_settings.get_can_send_messages(request.user)

    are_friends = Friend.objects.are_friends(request.user, user)

    friend_request_sent = False
    if not are_friends:
        friend_request_sent = request.user.friendship_requests_sent.filter(
            to_user=user
        ).first()

    sections = []
    connection = request.user.get_connection_to(user)
    friends = None
    pinboard_page_obj = None

    if can_see_profile:
        sections = filter(
            lambda x: x is not None,
            [
                make_section(_("General"), ["nickname", "pronouns", "birthday"]),
                make_section(
                    _("Personal"),
                    [
                        "mothers_maiden_name",
                        "name_of_first_pet",
                        "grew_up_street",
                        "first_car_make",
                        "looking_for",
                        "relationship",
                        "hobbies",
                        "what_i_like",
                        "what_i_dont_like",
                        "favourite_music",
                        "favourite_movies",
                        "favourite_books",
                        "favourite_food",
                        "i_am_good_at",
                        "i_wish_for",
                    ],
                ),
            ],
        )

        friends = Friend.objects.friends(user)

        pinboard_items = user.pinboard.order_by("-created_at")
        pinboard_paginator = Paginator(pinboard_items, 5)
        pinboard_page_obj = pinboard_paginator.get_page(1)

    ctx = {
        "user": user,
        "current": request.user == user,
        "sections": sections,
        "friends": friends,
        "are_friends": are_friends,
        "friend_request_sent": friend_request_sent,
        "connection": connection,
        "pinboard_page_obj": pinboard_page_obj,
        "can_see_profile": can_see_profile,
        "can_send_messages": can_send_messages,
    }

    return render(request, "core/user_detail.html", ctx)


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    model = User
    success_message = _("Profile successfully updated")
    success_url = reverse_lazy("profile-update")

    def get_object(self):
        return self.request.user


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
