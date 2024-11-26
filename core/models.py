from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from friendship.models import Friend
from uuid import uuid4


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    @property
    def display_name(self):
        full_name = self.profile.full_name
        if full_name and len(full_name.strip()) > 0:
            return full_name
        else:
            return self.username

    def get_connection_to(self, other_user):
        if self == other_user:
            return []

        if Friend.objects.are_friends(self, other_user):
            return [other_user]

        # one intermediate
        intermediates = Friend.objects.filter(to_user=other_user).filter(
            from_user__friends__from_user=self
        )

        intermediate = intermediates.first()
        if intermediate:
            return [intermediate.from_user, other_user]

        return []

    def get_friends_of_friends(self):
        friends_reverse = Friend.objects.filter(from_user=self)

        fof = (
            User.objects
            # Friends of friends
            .filter(friends__from_user__friends__in=friends_reverse)
            .filter(~Q(friends__in=friends_reverse))
            .filter(~Q(id=self.id))
            # Mutual friends count
            .annotate(
                mutual_friends=Q(friends__from_user__friends__from_user=self),
            )
            .annotate(mutual_friends_count=Count("mutual_friends"))
            .order_by("-mutual_friends_count")
        )

        return fof

    def get_absolute_url(self):
        return reverse("profile", kwargs={"id": self.id})

    def __str__(self):
        return self.display_name
