from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView

from .models import User
from .forms import ProfileForm


def index(request: HttpRequest):
    return render(request, "core/index.html", {})


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

    sections = filter(
        lambda x: x is not None,
        [
            make_section(_("General"), ["nickname", "pronouns", "birthday"]),
            make_section(
                _("Personal"),
                [
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

    ctx = {"user": user, "current": request.user == user, "sections": sections}

    return render(request, "core/user_detail.html", ctx)


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    model = User
    success_message = _("Profile successfully updated")
    success_url = reverse_lazy("profile-update")

    def get_object(self):
        return self.request.user
