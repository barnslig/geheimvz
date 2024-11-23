from django.urls import path

from .views import invite_code_list


urlpatterns = [
    path("my-invites.php", invite_code_list, name="invite_code_list"),
]
