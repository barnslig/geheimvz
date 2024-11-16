from django.urls import path

from .views import (
    index,
    index_login,
    info,
)


urlpatterns = [
    path("", index, name="index"),
    path("start.php", index_login, name="index-login"),
    path("info.php", info),
]
