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
from django.urls import include, path
from pictures.conf import get_settings

from core import views as core_views

urlpatterns = [
    path("", core_views.index),
    path("profile.php/<str:id>", core_views.profile, name="profile"),
    path(
        "edit-profile.php",
        core_views.ProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()

if get_settings().USE_PLACEHOLDERS:
    urlpatterns += [
        path("_pictures/", include("pictures.urls")),
    ]
