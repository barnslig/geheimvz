"""
URL configuration for geheimvz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from core import urls as core_urls
from friends import urls as friends_urls
from groups import urls as groups_urls
from invites import urls as invites_urls
from my_account import urls as my_account_urls
from my_profile import urls as my_profile_urls
from pinboard import urls as pinboard_urls
from private_messages import urls as private_messages_urls
from search import urls as search_urls

urlpatterns = [
    # Auth
    path("logout.php", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "pw-reset.php",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "pw-reset-done.php",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "pw-reset.php/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "pw-reset-complete.php",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Admin
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path("healthz/", include("health_check.urls")),
]

urlpatterns += core_urls.urlpatterns
urlpatterns += friends_urls.urlpatterns
urlpatterns += groups_urls.urlpatterns
urlpatterns += invites_urls.urlpatterns
urlpatterns += my_account_urls.urlpatterns
urlpatterns += my_profile_urls.urlpatterns
urlpatterns += pinboard_urls.urlpatterns
urlpatterns += private_messages_urls.urlpatterns
urlpatterns += search_urls.urlpatterns
urlpatterns += debug_toolbar_urls()
