from django.urls import path

from .views import pinboard_delete, pinboard_list, pinboard_create

urlpatterns = [
    path("pinnwand.php/<str:pk>", pinboard_list, name="pinboard"),
    path(
        "pinnnwand-write.php/<str:pk>",
        pinboard_create,
        name="pinboard-create",
    ),
    path("pinnwand-loeschen.php/<str:pk>", pinboard_delete, name="pinboard_delete"),
]
