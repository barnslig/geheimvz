from django.urls import path

from .views import (
    profile,
    ProfileUpdateView,
)


urlpatterns = [
    path("profile.php/<str:id>", profile, name="profile"),
    path("edit-profile.php", ProfileUpdateView.as_view(), name="profile-update"),
]
