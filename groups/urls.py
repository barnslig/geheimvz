from django.urls import path

from .views import (
    GroupCreateView,
    GroupDetailView,
    GroupListAllView,
    GroupListView,
    GroupUpdateView,
    forumpost_create,
    forumthread_create,
    forumthread_detail,
    forumthread_list,
    group_invite_reject,
    group_invite,
    group_join,
    group_leave,
    group_list_invites,
)

urlpatterns = [
    path("group.php/<str:pk>", GroupDetailView.as_view(), name="group"),
    path("leave-group.php/<str:pk>", group_leave, name="group-leave"),
    path("join-group.php/<str:pk>", group_join, name="group-join"),
    path("my-groups.php", GroupListView.as_view(), name="groups"),
    path("all-groups.php", GroupListAllView.as_view(), name="groups-all"),
    path("group-invitations.php", group_list_invites, name="group-invitations"),
    path("invite-to-group.php/<str:pk>", group_invite, name="group-invite"),
    path("reject-invite.php/<str:pk>", group_invite_reject, name="group-invite-reject"),
    path("new-group.php", GroupCreateView.as_view(), name="group-create"),
    path("edit-group.php/<str:pk>", GroupUpdateView.as_view(), name="group-update"),
    path("viewtopics.php/<str:pk>", forumthread_list, name="forumthread_list"),
    path("viewtopic.php/<str:pk>", forumthread_detail, name="forumthread_detail"),
    path("new-thread.php/<str:pk>", forumthread_create, name="forumthread_create"),
    path("new-post.php/<str:pk>", forumpost_create, name="forumpost_create"),
]
