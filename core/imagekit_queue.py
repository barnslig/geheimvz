from django.apps import apps as django_apps
from dramatiq import actor
from imagekit.cachefiles import ImageCacheFile
from imagekit.cachefiles.backends import BaseAsync
from imagekit.registry import generator_registry
from imagekit.utils import get_singleton, get_storage


def get_full_qualified(instance):
    return f"{type(instance).__module__}.{type(instance).__name__}"


def imagekit_dumps(i: ImageCacheFile):
    generator_id = next(
        id
        for id, generator in generator_registry._generators.items()
        if generator == type(i.generator)
    )

    source = i.generator.source

    return {
        "source_model": f"{source.instance._meta.app_label}.{source.instance._meta.object_name}",
        "source_pk": str(source.instance.pk),
        "source_field": source.field.attname,
        "generator": generator_id,
        "name": i.name,
        "cachefile_backend": get_full_qualified(i.cachefile_backend),
        "cachefile_strategy": get_full_qualified(i.cachefile_strategy),
    }


def imagekit_loads(obj):
    SourceModel = django_apps.get_model(obj["source_model"])
    source_instance = SourceModel.objects.get(pk=obj["source_pk"])
    source = getattr(source_instance, obj["source_field"])

    generator = generator_registry.get(obj["generator"], source=source)

    return ImageCacheFile(
        generator,
        obj["name"],
        get_storage(),
        get_singleton(obj["cachefile_backend"], "cache file backend"),
        get_singleton(obj["cachefile_strategy"], "cache file strategy"),
    )


@actor
def _imagekit_generate_file(force=False, **args):
    file = imagekit_loads(args)
    file.cachefile_backend.generate_now(file, force=force)


# See https://github.com/matthewwithanm/django-imagekit/issues/510
class Dramatiq(BaseAsync):
    def schedule_generation(self, file, force=False):
        args = imagekit_dumps(file)
        _imagekit_generate_file.send(force=force, **args)
