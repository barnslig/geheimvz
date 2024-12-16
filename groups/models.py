from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField, ImageSpecField
import uuid

from core.helpers import (
    UploadToUuidFilename,
    ValidateImageAspectRatio,
    ValidateImageSize,
    ValidateMaxFilesize,
)
from core.imagegenerators import ProfileKeep
from .imagegenerators import AttachmentSpec


User = get_user_model()


class GroupManager(models.Manager):
    def popular(self, for_user):
        return (
            Group.objects.exclude(members__in=[for_user])
            .annotate(friends_count=Count(Q(members__friends__from_user=for_user)))
            .annotate(members_count=Count("members"))
            .order_by("-friends_count", "-members_count")
        )


class Group(models.Model):
    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    objects = GroupManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Created by"),
    )

    image_height = models.PositiveIntegerField(blank=True, null=True)
    image_width = models.PositiveIntegerField(blank=True, null=True)
    image = ProcessedImageField(
        spec=ProfileKeep,
        null=True,
        blank=True,
        width_field="image_width",
        height_field="image_height",
        upload_to=UploadToUuidFilename("groups/"),
        validators=[
            ValidateMaxFilesize(10),
            ValidateImageSize(100, 100, 10000, 10000),
            ValidateImageAspectRatio(0.5, 1.8),
        ],
        verbose_name=_("Group picture"),
    )
    image_profile_medium = ImageSpecField(
        source="image",
        id="geheimvz:core:profile_medium",
    )

    # Members
    members = models.ManyToManyField(
        User, related_name="groups_member", verbose_name=_("Members")
    )

    # Admins
    admins = models.ManyToManyField(
        User, related_name="groups_admin", verbose_name=_("Admins")
    )

    # Meta
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    has_forum = models.BooleanField(default=True, verbose_name=_("Enable forum"))
    is_private = models.BooleanField(default=False, verbose_name=_("Is invite-only"))

    def get_can_create_thread(self, user):
        return self.members.contains(user) or self.admins.contains(user)

    def get_can_invite(self, user):
        return self.members.contains(user) or self.admins.contains(user)

    def get_absolute_url(self):
        return reverse("group", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class GroupInvitation(models.Model):
    class Meta:
        verbose_name = _("Group invitation")
        verbose_name_plural = _("Group invitations")

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_invitations_sent",
        verbose_name=_("Sender"),
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_invitations_received",
        verbose_name=_("Recipient"),
    )
    for_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="invitations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.to_user.display_name} invited to group {self.for_group.name} by {self.from_user.display_name}"


class ForumThread(models.Model):
    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Created by"),
    )
    group = models.ForeignKey(
        Group,
        related_name="threads",
        on_delete=models.CASCADE,
        verbose_name=_("Group"),
    )

    topic = models.CharField(max_length=255, unique=True, verbose_name=_("Topic"))

    def get_can_create_post(self, user):
        return self.group.members.contains(user) or self.group.admins.contains(user)

    def get_absolute_url(self):
        return reverse("forumthread_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.topic


class ForumPost(models.Model):
    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Created by"),
    )
    thread = models.ForeignKey(
        ForumThread,
        related_name="posts",
        on_delete=models.CASCADE,
        verbose_name=_("Thread"),
    )

    post = models.TextField(verbose_name=_("Post"))

    attachment_height = models.PositiveIntegerField(blank=True, null=True)
    attachment_width = models.PositiveIntegerField(blank=True, null=True)
    attachment = ProcessedImageField(
        spec=AttachmentSpec,
        null=True,
        blank=True,
        width_field="attachment_width",
        height_field="attachment_height",
        upload_to=UploadToUuidFilename("groups/attachments/"),
        validators=[
            ValidateMaxFilesize(10),
            ValidateImageSize(100, 100, 10000, 10000),
            ValidateImageAspectRatio(0.5, 1.8),
        ],
        verbose_name=_("Attachment"),
    )
    attachment_thumbnail = ImageSpecField(
        source="attachment",
        id="geheimvz:groups:attachment_thumbnail",
    )
