from django.db import models
from django.utils.timezone import now


class AuthorizationRequestUnit(models.Model):
    authorization_request = models.ForeignKey(
        "authorization_requests.AuthorizationRequest", on_delete=models.CASCADE
    )
    document = models.TextField(max_length=256)
    pages = models.IntegerField(default=1, null=False, blank=False)
    copies = models.IntegerField(default=1, null=False, blank=False)
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("checked", "Checked"),
    )

    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="pending")


class AuthorizationRequest(models.Model):
    requester = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.CASCADE)
    documents = models.ManyToManyField(
        "authorization_requests.AuthorizationRequestUnit")
    date_requested = models.DateTimeField(default=now, editable=False)
    college = models.CharField(max_length=64, blank=False, null=False)
    purpose = models.TextField(max_length=512, blank=False, null=False)

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
        ("claimed", "Claimed"),
        ("unclaimed", "Unclaimed"),
    )

    remarks = models.TextField(max_length=512, blank=True, null=True)

    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default="pending")
