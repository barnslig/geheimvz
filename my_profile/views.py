from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import UpdateView
from friendship.models import Friend

from .forms import ProfileForm
from .models import MyProfile

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

    return render(request, "my_profile/myprofile_detail.html", ctx)


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    model = MyProfile
    success_message = _("Profile successfully updated")
    success_url = reverse_lazy("profile-update")

    def get_object(self):
        return self.request.user.profile
