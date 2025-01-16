from django.db import models
from django.utils.timezone import now


class AuthorizationRequest(models.Model):
    requester = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE)
    documents = models.TextField(max_length=2048, blank=False, null=False)
    date_requested = models.DateTimeField(default=now, editable=False)
    college = models.CharField(max_length=64, blank=False, null=False)
    purpose = models.TextField(max_length=512, blank=False, null=False)

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
    )

    remarks = models.TextField(max_length=512, blank=True, null=True)

    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="pending")