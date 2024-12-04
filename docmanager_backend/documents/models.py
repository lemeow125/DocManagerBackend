from django.db import models
from django.utils.timezone import now
import uuid


class Document(models.Model):
    name = models.CharField(max_length=100)

    document_type = models.CharField(
        max_length=128, null=False, blank=False
    )
    number_pages = models.IntegerField(null=False, blank=False)
    ocr_metadata = models.TextField(null=True, blank=True)

    def upload_to(instance, filename):
        _, extension = filename.rsplit(".", 1)
        return "documents/%s_%s.%s" % (now(), str(uuid.uuid4()), extension)

    file = models.FileField(upload_to=upload_to)

    date_uploaded = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return f"{self.name} ({self.document_type})"
