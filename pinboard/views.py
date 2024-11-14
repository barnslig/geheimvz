from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import PinboardMessageForm
from .models import PinboardMessage
from .tasks import send_on_create_mail

User = get_user_model()


@login_required
def pinboard_list(request: HttpRequest, pk: str):
    user = get_object_or_404(User, pk=pk)

    if not user.privacy_settings.get_can_see_profile(request.user):
        raise PermissionDenied()

    posts = user.pinboard.order_by("-created_at")
    posts_paginator = Paginator(posts, 20)
    posts_page_obj = posts_paginator.get_page(request.GET.get("page", 1))

    ctx = {
        "page_obj": posts_page_obj,
        "user": user,
    }

    return render(request, "pinboard/pinboardmessage_list.html", ctx)


@ratelimit(key="user", rate="1/m", method="POST")
@ratelimit(key="user", rate="20/d", method="POST")
@login_required
def pinboard_create(request: HttpRequest, pk: str):
    user = get_object_or_404(User, pk=pk)

    if not user.privacy_settings.get_can_see_profile(request.user):
        raise PermissionDenied()

    if request.method == "POST":
        instance = PinboardMessage()
        instance.created_by = request.user
        instance.created_for = user

        form = PinboardMessageForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Successfully posted to pinboard"),
            )

            if user.notification_settings.on_new_pinboard_message:
                send_on_create_mail.delay(
                    request.user.display_name,
                    user.display_name,
                    user.email,
                )

            return redirect(user)
    else:
        form = PinboardMessageForm()

    ctx = {
        "user": user,
        "form": form,
    }

    return render(request, "pinboard/pinboardmessage_form.html", ctx)


@login_required
def pinboard_delete(request: HttpRequest, pk: str):
    post = get_object_or_404(PinboardMessage, pk=pk)

    if not post.get_can_delete_post(request.user):
        raise PermissionDenied()

    if request.method == "POST":
        post.delete()

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Post successfully deleted"),
        )

        return redirect("pinboard", pk=post.created_for.pk)

    created_by_name = post.created_by.display_name

    ctx = {
        "headline": _("Delete %(name)s post from your pinboard")
        % {"name": created_by_name},
        "copy": _(
            "Are you sure that you want to delete %(name)s's post from your pinboard?"
        )
        % {"name": created_by_name},
        "cancel_href": reverse_lazy("pinboard", kwargs={"pk": request.user.pk}),
    }

    return render(request, "core/confirmation.html", ctx)
