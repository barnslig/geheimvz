from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit, Transpose

from core.imagegenerators import StripMetadata


class AttachmentSpec(ImageSpec):
    processors = [
        Transpose(Transpose.AUTO),
        ResizeToFit(width=3000),
        StripMetadata(),
    ]
    format = "avif"
    options = {"quality": 65, "speed": 9}


class AttachmentThumbnailSpec(ImageSpec):
    processors = [
        Transpose(Transpose.AUTO),
        ResizeToFit(width=500),
        StripMetadata(),
    ]
    format = "avif"
    options = {"quality": 65, "speed": 9}


register.generator("geheimvz:groups:attachment_thumbnail", AttachmentThumbnailSpec)
