from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from notifications.models import Notification
from django.utils import timezone


@receiver(post_save, sender=Notification)
def notification_post_save(sender, instance, **kwargs):
    # Calculate the time threshold (15 minutes ago)
    threshold = timezone.now() - timedelta(minutes=15)

    # Find and delete all notifications older than 15 minutes
    Notification.objects.filter(timestamp__lt=threshold).delete()
