from django.urls import path

from .views import (
    friend_add,
    friend_remove,
    friend_list,
    friend_requests,
    friend_requests_sent,
    friend_suggestions,
    friendship_accept,
    friendship_cancel,
    friendship_reject,
)

urlpatterns = [
    path("add-friend-v2.php/<str:pk>", friend_add, name="friend-add"),
    path("remove-friend.php/<str:pk>", friend_remove, name="friend-remove"),
    path("friends-old.php", friend_list, name="friends"),
    path("friend-requests.php", friend_requests, name="friend-requests"),
    path("friend-suggestions.php", friend_suggestions, name="friend-suggestions"),
    path("friend-req-sent.php", friend_requests_sent, name="friend-requests-sent"),
    path("friend-req-accept.php/<int:pk>", friendship_accept, name="friendship_accept"),
    path("friend-req-reject.php/<int:pk>", friendship_reject, name="friendship_reject"),
    path("friend-req-cancel.php/<int:pk>", friendship_cancel, name="friendship_cancel"),
]
