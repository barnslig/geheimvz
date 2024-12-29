from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic.edit import UpdateView
from friendship.models import Friend

from .forms import ProfileForm
from .models import Greeting, MyProfile
from .tasks import send_on_greeting_mail

User = get_user_model()


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
            label = user.profile._meta.get_field(field).verbose_name
            value = getattr(user.profile, field)
            if not is_empty(value):
                section["fields"].append({"label": label, "value": value})

        if len(section["fields"]) > 0:
            return section

        return None

    can_see_profile = user.privacy_settings.get_can_see_profile(request.user)
    can_send_messages = user.privacy_settings.get_can_send_messages(request.user)

    are_friends = Friend.objects.are_friends(request.user, user)

    friend_request_sent = False
    friend_request_received = False
    if not are_friends:
        friend_request_sent = request.user.friendship_requests_sent.filter(
            to_user=user
        ).first()
        friend_request_received = user.friendship_requests_sent.filter(
            to_user=request.user
        ).first()

    sections = []
    connection = request.user.get_connection_to(user)
    groups = None
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

        groups = user.groups_member.order_by("name")

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
        "friend_request_received": friend_request_received,
        "connection": connection,
        "groups": groups,
        "pinboard_page_obj": pinboard_page_obj,
        "can_see_profile": can_see_profile,
        "can_send_messages": can_send_messages,
    }

    return render(request, "my_profile/myprofile_detail.html", ctx)


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    model = MyProfile
    success_message = _("Profile successfully updated")
    success_url = reverse_lazy("profile-update")

    def get_object(self):
        return self.request.user.profile


@login_required
@ratelimit(key="user", rate="4/m", method="POST")
@ratelimit(key="user", rate="200/d", method="POST")
@require_POST
def greeting_create(request: HttpRequest, pk: str):
    to_friend = get_object_or_404(request.user.friends, from_user__pk=pk)
    to_user = to_friend.from_user

    already_greeted = to_user.greetings_received.filter(from_user=request.user).exists()

    if already_greeted:
        messages.add_message(
            request,
            messages.ERROR,
            request.user.profile.greeting_i18n["error"](to_user.display_name),
        )
    else:
        greeting = Greeting()
        greeting.from_user = request.user
        greeting.to_user = to_user
        greeting.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            request.user.profile.greeting_i18n["success"](to_user.display_name),
        )

        if to_user.notification_settings.on_new_greeting:
            send_on_greeting_mail.send(str(request.user.pk), str(to_user.pk))

    return redirect("profile", id=to_user.pk)


@login_required
@require_POST
def greeting_remove(request: HttpRequest, pk: int):
    greeting = get_object_or_404(request.user.greetings_received, pk=pk)
    greeting.delete()
    return redirect("index-login")
