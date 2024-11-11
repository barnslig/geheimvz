from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit, Transpose
from PIL import Image


class StripMetadata(object):
    def process(self, image: Image):
        image.info = {}
        return image


class ProfileKeep(ImageSpec):
    processors = [
        Transpose(Transpose.AUTO),
        StripMetadata(),
    ]
    format = "avif"
    options = {"quality": 65, "speed": 9}


class ProfileMedium(ImageSpec):
    processors = [
        Transpose(Transpose.AUTO),
        ResizeToFit(width=500),
        StripMetadata(),
    ]
    format = "avif"
    options = {"quality": 65, "speed": 9}


class ProfileSmall(ImageSpec):
    processors = [
        Transpose(Transpose.AUTO),
        ResizeToFit(width=140),
        StripMetadata(),
    ]
    format = "avif"
    options = {"quality": 65, "speed": 9}


register.generator("geheimvz:core:profile_medium", ProfileMedium)
register.generator("geheimvz:core:profile_small", ProfileSmall)
