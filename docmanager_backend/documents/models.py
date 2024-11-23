from django.db import models
from django.utils.timezone import now
import uuid


class Document(models.Model):
    name = models.CharField(max_length=100)

    DOCUMENT_TYPE_CHOICES = (
        ("pdf", "PDF"),
        ("image", "Image"),
        ("video", "Video"),
        ("doc", "Word Document"),
        ("excel", "Excel Document"),
        ("ppt", "Powerpoint Document"),
    )
    document_type = models.CharField(
        max_length=32, choices=DOCUMENT_TYPE_CHOICES, null=False, blank=False
    )
    number_pages = models.IntegerField(null=False, blank=False)

    def upload_to(instance, filename):
        _, extension = filename.split(".")
        return "documents/%s_%s.%s" % (now(), str(uuid.uuid4()), extension)

    file = models.FileField(upload_to=upload_to)

    date_uploaded = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.name} ({self.document_type})"
