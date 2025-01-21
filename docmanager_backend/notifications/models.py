from django.db import models
from django.utils.timezone import now


class Notification(models.Model):
    client = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=now, editable=False)

    content = models.TextField(max_length=512, blank=True, null=True)

    AUDIENCE_CHOICES = (
        ("client", "Client"),
        ("staff", "Staff"),
        ("head", "Head")
    )

    TYPE_CHOICES = (
        ("info", "Info"),
        ("warning", "Warning"),
    )

    type = models.CharField(
        max_length=16, choices=TYPE_CHOICES, default="info")

    audience = models.CharField(
        max_length=16, choices=AUDIENCE_CHOICES, default="staff")
