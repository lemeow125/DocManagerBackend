from django.db import models
from django.utils.timezone import now


class DocumentRequestUnit(models.Model):
    document_request = models.ForeignKey(
        "document_requests.DocumentRequest", on_delete=models.CASCADE
    )
    document = models.ForeignKey("documents.Document", on_delete=models.CASCADE)
    copies = models.IntegerField(default=1, null=False, blank=False)


class DocumentRequest(models.Model):
    requester = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    documents = models.ManyToManyField("document_requests.DocumentRequestUnit")
    date_requested = models.DateTimeField(default=now, editable=False)
    college = models.CharField(max_length=64, blank=False, null=False)
    purpose = models.TextField(max_length=512, blank=False, null=False)

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("denied", "Denied"),
    )

    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")

    # TODO: Add request type (Softcopy/Hardcopy)
