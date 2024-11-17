from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from friendship.models import Friend

User = get_user_model()


class AppearanceSettings(models.Model):
    class ColorChoices(models.TextChoices):
        ROSE = "theme-rose", _("Rose")
        BLUE = "theme-blue", _("Blue")
        GREEN = "theme-green", _("Green")
        DARK = "theme-dark", _("Dark Mode")
        CONTRAST = "theme-contrast", _("High Contrast")

    class FontChoices(models.TextChoices):
        SANS = "font-sans", _("Sans-Serif")
        SERIF = "font-serif", _("Serif")
        MONO = "font-mono", _("Monospace")
        COMIC = "font-comic", _("Comic")
        # SLAB
        # CUTE
        # FUTURISTIC
        # PIXEL

    class BackgroundChoices(models.TextChoices):
        NONE = "NONE", _("None")
        CLOUDS = "CLOUDS", _("Clouds")
        CHARLIE = "CHARLIE", _("Charlie Brown")
        WAVES = "WAVES", _("Waves")

    class LogoChoices(models.TextChoices):
        SIMPLE = "SIMPLE", _("Simple")
        PRIDE = "PRIDE", _("Pride")
        EYE = "EYE", _("All-Seeing Eye")

    class SizeChoices(models.TextChoices):
        XS = "size-xs", _("Extra Small")
        SM = "size-sm", _("Small")
        BASE = "size-base", _("Default")
        LG = "size-lg", _("Large")

    owner = AutoOneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="appearance_settings",
    )
    color = models.CharField(
        max_length=255,
        choices=ColorChoices,
        default=ColorChoices.ROSE,
        verbose_name=_("Theme color"),
    )
    font = models.CharField(
        max_length=255,
        choices=FontChoices,
        default=FontChoices.SANS,
        verbose_name=_("Theme font"),
    )
    size = models.CharField(
        max_length=255,
        choices=SizeChoices,
        default=SizeChoices.BASE,
        verbose_name=_("Theme size"),
    )
    background = models.CharField(
        max_length=255,
        choices=BackgroundChoices,
        default=BackgroundChoices.NONE,
        verbose_name=_("Theme background"),
    )
    logo = models.CharField(
        max_length=255,
        choices=LogoChoices,
        default=LogoChoices.SIMPLE,
        verbose_name=_("Theme logo"),
    )

    def __str__(self):
        return f"Settings for {self.owner.display_name}"


class NotificationSettings(models.Model):
    owner = AutoOneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )

    on_new_pinboard_message = models.BooleanField(
        default=True,
        verbose_name=_("On new pinboard message"),
    )
    on_new_private_message = models.BooleanField(
        default=True,
        verbose_name=_("On new private message"),
    )
    on_new_friend_request = models.BooleanField(
        default=True,
        verbose_name=_("On new friend request"),
    )
    on_new_group_invitation = models.BooleanField(
        default=True,
        verbose_name=_("On new group invitation"),
    )
    on_new_greeting = models.BooleanField(
        default=True,
        verbose_name=_("On new greetings"),
    )

    def __str__(self):
        return f"Settings for {self.owner.display_name}"


class PrivacySettings(models.Model):
    class PrivacyChoices(models.TextChoices):
        EVERYONE = "E", _("Everyone logged in")
        FRIENDS = "F", _("Only my friends")

    owner = AutoOneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="privacy_settings",
    )

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

    def get_can_see_profile(self, user):
        if self.can_see_profile == PrivacySettings.PrivacyChoices.EVERYONE:
            return True

        if user == self.owner:
            return True

        if Friend.objects.are_friends(self.owner, user):
            return True

        if user.is_superuser:
            return True

        return False

    def get_can_send_messages(self, user):
        if self.can_send_messages == PrivacySettings.PrivacyChoices.EVERYONE:
            return True

        if Friend.objects.are_friends(self.owner, user):
            return True

        if user.friendship_requests_sent.filter(to_user=user).exists():
            return True

        if user.is_superuser:
            return True

        return False

    def __str__(self):
        return f"Settings for {self.owner.display_name}"
