from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from friendship.models import Friend
from imagekit.models import ProcessedImageField, ImageSpecField
from uuid import uuid4

from .helpers import (
    UploadToUuidFilename,
    ValidateImageAspectRatio,
    ValidateImageSize,
    ValidateMaxFilesize,
)
from .imagegenerators import ProfileKeep


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    image_height = models.PositiveIntegerField(blank=True, null=True)
    image_width = models.PositiveIntegerField(blank=True, null=True)
    image = ProcessedImageField(
        spec=ProfileKeep,
        null=True,
        blank=True,
        width_field="image_width",
        height_field="image_height",
        upload_to=UploadToUuidFilename("profiles/"),
        validators=[
            ValidateMaxFilesize(10),
            ValidateImageSize(100, 100, 4000, 4000),
            ValidateImageAspectRatio(0.5, 1.8),
        ],
        verbose_name=_("Profile picture"),
    )
    image_profile_medium = ImageSpecField(
        source="image",
        id="geheimvz:core:profile_medium",
    )
    image_profile_small = ImageSpecField(
        source="image",
        id="geheimvz:core:profile_small",
    )

    # Account
    full_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Full name")
    )
    nickname = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Nickname")
    )
    pronouns = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Pronouns")
    )
    birthday = models.DateField(null=True, blank=True, verbose_name=_("Birthday"))

    # Personal
    mothers_maiden_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Your mother's maiden name"),
    )
    name_of_first_pet = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Name of your first pet")
    )
    grew_up_street = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Street where you grew up"),
    )
    first_car_make = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Make of your first car")
    )
    looking_for = models.TextField(null=True, blank=True, verbose_name=_("Looking for"))
    relationship = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Relationship")
    )
    hobbies = models.TextField(null=True, blank=True, verbose_name=_("Hobbies"))
    what_i_like = models.TextField(null=True, blank=True, verbose_name=_("What I like"))
    what_i_dont_like = models.TextField(
        null=True, blank=True, verbose_name=_("What I don't like")
    )
    favourite_music = models.TextField(
        null=True, blank=True, verbose_name=_("Favourite music")
    )
    favourite_movies = models.TextField(
        null=True, blank=True, verbose_name=_("Favourite movies")
    )
    favourite_books = models.TextField(
        null=True, blank=True, verbose_name=_("Favourite books")
    )
    favourite_food = models.TextField(
        null=True, blank=True, verbose_name=_("Favourite food")
    )
    i_am_good_at = models.TextField(
        null=True, blank=True, verbose_name=_("I am good at")
    )
    i_wish_for = models.TextField(null=True, blank=True, verbose_name=_("I wish for"))

    # privacy settings
    class PrivacyChoices(models.TextChoices):
        EVERYONE = "E", _("Everyone logged in")
        FRIENDS = "F", _("Only my friends")

    can_see_profile = models.CharField(
        max_length=1,
        choices=PrivacyChoices,
        default=PrivacyChoices.FRIENDS,
        verbose_name=_("Who can see your page?"),
    )
    can_send_messages = models.CharField(
        max_length=1,
        choices=PrivacyChoices,
        default=PrivacyChoices.FRIENDS,
        verbose_name=_("Who can send you messages?"),
    )

    @property
    def display_name(self):
        if self.full_name and len(self.full_name) > 0:
            return self.full_name
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

    def get_can_see_profile(self, user):
        if self.can_see_profile == User.PrivacyChoices.EVERYONE:
            return True

        if user == self:
            return True

        if Friend.objects.are_friends(self, user):
            return True

        if user.is_superuser:
            return True

        return False

    def get_can_send_messages(self, user):
        if self.can_send_messages == User.PrivacyChoices.EVERYONE:
            return True

        if Friend.objects.are_friends(self, user):
            return True

        if user.friendship_requests_sent.filter(to_user=user).exists():
            return True

        if user.is_superuser:
            return True

        return False

    def get_absolute_url(self):
        return reverse("profile", kwargs={"id": self.id})

    def __str__(self):
        return self.display_name
