from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from .models import Property
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Property)
def property_saved(sender, instance, created, **kwargs):
    cache.delete('all_properties')