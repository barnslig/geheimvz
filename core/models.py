from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from pictures.models import PictureField
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    image_width = models.PositiveIntegerField(null=True)
    image_height = models.PositiveIntegerField(null=True)
    image = PictureField(
        null=True,
        blank=True,
        upload_to="profiles/",
        width_field="image_width",
        height_field="image_height",
        verbose_name=_("Profile picture"),
    )

    # Account
    nickname = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Nickname")
    )
    pronouns = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Pronouns")
    )
    birthday = models.DateField(null=True, blank=True, verbose_name=_("Birthday"))

    # Personal
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
