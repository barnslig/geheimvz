from django.urls import path

from .views import (
    PrivateMessageCreateView,
    PrivateMessageDetailView,
    PrivateMessageListSentView,
    PrivateMessageListView,
)

urlpatterns = [
    path("mails.php", PrivateMessageListView.as_view(), name="messages"),
    path(
        "message.php/<str:pk>",
        PrivateMessageDetailView.as_view(),
        name="message_detail",
    ),
    path("postausgang.php", PrivateMessageListSentView.as_view(), name="messages_sent"),
    path("new-messsage.php", PrivateMessageCreateView.as_view(), name="message_create"),
    path(
        "new-messsage.php/<str:pk>",
        PrivateMessageCreateView.as_view(),
        name="message_create_to",
    ),
]
