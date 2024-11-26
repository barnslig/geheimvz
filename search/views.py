from django_ratelimit.decorators import ratelimit
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render

from .tables import UserTable
from .forms import SearchForm

User = get_user_model()


@ratelimit(key="user", rate="2/m", method="POST")
@ratelimit(key="user", rate="100/d", method="POST")
@login_required
def search(request: HttpRequest):
    form = SearchForm(request.GET)

    users = None
    table = UserTable([])

    if form.is_valid():
        q = form.cleaned_data["q"]

        users = User.objects.filter(
            Q(profile__full_name__contains=q)
            | Q(username__contains=q)
            | Q(nickname__contains=q)
        )

        table = UserTable(users)

    ctx = {
        "form": form,
        "users": users,
        "table": table,
    }

    return render(request, "search/search_results.html", ctx)
