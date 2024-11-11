from django.core.exceptions import ValidationError
from django.db.models.fields import files
from django.utils.translation import gettext_lazy as _
from functools import wraps
from os.path import splitext, join
from uuid import uuid4
from django.utils.deconstruct import deconstructible


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
