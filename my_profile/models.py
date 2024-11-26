from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html
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
            ValidateImageSize(100, 100, 10000, 10000),
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

    # Greetings
    class GreetingChoices(models.TextChoices):
        GRUSCHELN = "GRUSCHELN", _("Gruscheln")  # Gruscheln
        NUDGE = "NUDGE", _("Nudge")  # Anstupsen
        MEOW = "MEOW", _("Meow")  # Maunzen
        WAVE = "WAVE", _("Wave")  # Winken

    greeting_word = models.CharField(
        max_length=255,
        choices=GreetingChoices,
        default=GreetingChoices.GRUSCHELN,
        verbose_name=_("Greeting word"),
    )

    # Account
    full_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Full name")
    )
    nickname = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("Nickname")
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

    greetings_i18n = {
        GreetingChoices.GRUSCHELN: {
            "subject": _("You have been gruscheled!"),
            "message": _("has gruscheled you!"),
            "action": _("Gruscheln"),
            "return": _("gruschel back"),
            "success": lambda name: _("You gruscheled %(name)s.") % {"name": name},
            "error": lambda name: _("You already gruscheled %(name)s!")
            % {"name": name},
        },
        GreetingChoices.NUDGE: {
            "subject": _("You have been nudged!"),
            "message": _("has nudged you!"),
            "action": _("Nudge"),
            "return": _("nudge back"),
            "success": lambda name: _("You nudged %(name)s.") % {"name": name},
            "error": lambda name: _("You already nudged %(name)s!") % {"name": name},
        },
        GreetingChoices.MEOW: {
            "subject": _("You have been meowed at!"),
            "message": _("has meowed at you!"),
            "action": _("Meow"),
            "return": _("meow back"),
            "success": lambda name: _("You meowed at %(name)s.") % {"name": name},
            "error": lambda name: _("You already meowed at %(name)s!") % {"name": name},
        },
        GreetingChoices.WAVE: {
            "subject": _("You have been waved at!"),
            "message": _("has waved at you!"),
            "action": _("Wave"),
            "return": _("wave back"),
            "success": lambda name: _("You waved at %(name)s.") % {"name": name},
            "error": lambda name: _("You already waved at %(name)s!") % {"name": name},
        },
    }

    @property
    def greeting_i18n(self):
        return self.greetings_i18n[self.greeting_word]

    def __str__(self):
        return f"Profile of {self.owner.display_name}"


class Greeting(models.Model):
    class Meta:
        verbose_name = _("Greeting")
        verbose_name_plural = _("Greetings")

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="greetings_sent",
        verbose_name=_("Sender"),
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="greetings_received",
        verbose_name=_("Recipient"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Greeting from {self.from_user.display_name} to {self.to_user.display_name}"
