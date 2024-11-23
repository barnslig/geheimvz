from django.core.exceptions import ValidationError
from django.db.models.fields import files
from django.utils.translation import gettext_lazy as _
from os.path import splitext, join
from uuid import uuid4
from django.utils.deconstruct import deconstructible

from core.models import User


@deconstructible
class UploadToUuidFilename:
    """
    Replace the upload_to filename with an uuid4
    """

    def __init__(self, prefix: str):
        self.prefix = prefix

    def __call__(self, instance, filename: str):
        ext = splitext(filename)[1]
        filename = f"{uuid4()}{ext.lower()}"
        return join(self.prefix, filename)


@deconstructible
class ValidateMaxFilesize:
    """
    Validate that the FieldFile file size is below max_MB megabytes
    """

    def __init__(self, max_MB: int):
        self.max_MB = max_MB

    def __call__(self, value: files.FieldFile):
        if value.size > self.max_MB * 1e6:
            raise ValidationError(
                _("Maximum file size of %(value)s MB exceeded!"),
                params={"value": self.max_MB},
            )


@deconstructible
class ValidateImageAspectRatio:
    """
    Validate that an ImageField image ratio is within given bounds
    """

    def __init__(self, min_ratio: int, max_ratio: int):
        self.min_ratio = min_ratio
        self.max_ratio = max_ratio

    def __call__(self, value: files.ImageFieldFile):
        ratio = value.height / value.width
        if ratio < self.min_ratio or ratio > self.max_ratio:
            raise ValidationError(_("Invalid image aspect ratio."))


@deconstructible
class ValidateImageSize:
    """
    Validate that an ImageField image width/height is within given bounds
    """

    def __init__(
        self, min_width: int, min_height: int, max_width: int, max_height: int
    ):
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height

    def __call__(self, value: files.ImageFieldFile):
        if (
            value.width < self.min_width
            or value.width > self.max_width
            or value.height < self.min_height
            or value.height > self.max_height
        ):
            raise ValidationError(
                _(
                    "Image size needs to be within %(min_width)sx%(min_height)s and %(max_width)sx%(max_height)s"
                )
                % {
                    "min_width": self.min_width,
                    "min_height": self.min_height,
                    "max_width": self.max_width,
                    "max_height": self.max_height,
                }
            )


def get_user_display_name(user: User):
    return user.display_name
