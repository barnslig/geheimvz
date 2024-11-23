from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required
def invite_code_list(request: HttpRequest):
    invites = request.user.invite_codes.filter(remaining__gt=0)
    ctx = {"invites": invites}
    return render(request, "invites/invite_code_list.html", ctx)
