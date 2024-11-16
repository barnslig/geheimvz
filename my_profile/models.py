from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField, ImageSpecField

from core.helpers import (
    UploadToUuidFilename,
    ValidateImageAspectRatio,
    ValidateImageSize,
    ValidateMaxFilesize,
)
from core.imagegenerators import ProfileKeep

User = get_user_model()


class MyProfile(models.Model):
    owner = AutoOneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

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

    def __str__(self):
        return f"Profile of {self.owner.display_name}"
