from django.urls import path

from .views import (
    AppearanceUpdateView,
    LoginView,
    NotificationSettingsUpdateView,
    PasswordChangeView,
    PrivacyUpdateView,
    UserDeleteView,
    ProfileUpdateView,
)

urlpatterns = [
    path("account.php", ProfileUpdateView.as_view(), name="account"),
    path("aussehen.php", AppearanceUpdateView.as_view(), name="account-appearance"),
    path(
        "emails.php",
        NotificationSettingsUpdateView.as_view(),
        name="account-notifications",
    ),
    path("privatsphaere.php", PrivacyUpdateView.as_view(), name="account-privacy"),
    path("account-loeschen.php", UserDeleteView.as_view(), name="account-delete"),
    path("pw-change.php", PasswordChangeView.as_view(), name="password_change"),
    path("login.php", LoginView.as_view(), name="login"),
]
