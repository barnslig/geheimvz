from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login

from account.models import NotificationSettings

from .forms import RegisterForm
from .models import InviteCode


@login_required
def invite_code_list(request: HttpRequest):
    invites = request.user.invite_codes.filter(remaining__gt=0)
    ctx = {"invites": invites}
    return render(request, "invites/invite_code_list.html", ctx)


@user_passes_test(lambda u: u.is_anonymous)
def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                code = form.cleaned_data["code"]

                invite = get_object_or_404(InviteCode, code=code)
                invite.remaining -= 1
                invite.save()

                user = form.save()

                s = NotificationSettings(owner=user)
                s.save()

            login(request, user)
            return redirect("index-login")

    else:
        form = RegisterForm()

    ctx = {"form": form}
    return render(request, "invites/register.html", ctx)
