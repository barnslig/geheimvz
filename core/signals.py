from django_cleanup.signals import cleanup_pre_delete
from django.dispatch import receiver
from imagekit.cachefiles import LazyImageCacheFile
from imagekit.registry import generator_registry
from imagekit.utils import get_cache


@receiver(cleanup_pre_delete)
def imagekit_cache_cleanup(file, **kwargs):
    for id in generator_registry.get_ids():
        image = LazyImageCacheFile(id, source=file)
        cache_key = image.cachefile_backend.get_key(image)
        get_cache().delete(cache_key)
        image.storage.delete(image.name)
