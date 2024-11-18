from django.urls import path

from .views import (
    greeting_create,
    greeting_remove,
    profile,
    ProfileUpdateView,
)


urlpatterns = [
    path("profile.php/<str:id>", profile, name="profile"),
    path("edit-profile.php", ProfileUpdateView.as_view(), name="profile-update"),
    path("gruessen.php/<str:pk>", greeting_create, name="greeting_create"),
    path("gruss-ausblenden.php/<int:pk>", greeting_remove, name="greeting_remove"),
]
