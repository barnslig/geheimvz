from django.urls import path

from .views import (
    index,
    index_login,
    profile,
    ProfileUpdateView,
    info,
)


urlpatterns = [
    path("", index, name="index"),
    path("start.php", index_login, name="index-login"),
    path("profile.php/<str:id>", profile, name="profile"),
    path("edit-profile.php", ProfileUpdateView.as_view(), name="profile-update"),
    path("info.php", info),
]
