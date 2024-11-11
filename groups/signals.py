from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ForumPost, ForumThread


@receiver(post_save, sender=ForumThread)
def update_group_on_thread_save(sender, instance: ForumThread, **kwargs):
    instance.group.save()


@receiver(post_save, sender=ForumPost)
def update_thread_on_post_save(sender, instance: ForumPost, **kwargs):
    instance.thread.save()
