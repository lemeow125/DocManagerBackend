from django.db.models.signals import post_save
from django.dispatch import receiver
from config.settings import MEDIA_ROOT
import os
import fitz
import pytesseract
from PIL import Image
from .models import Document


@receiver(post_save, sender=Document)
def domain_post_save(sender, instance, **kwargs):
    if not instance.ocr_metadata:
        metadata = ""
        with fitz.open(os.path.join(MEDIA_ROOT, instance.file.name)) as doc:
            mat = fitz.Matrix(1.2, 1.2)
            for page in doc:
                pix = page.get_pixmap(matrix=mat)
                output = f'{page.number}.jpg'
                pix.save(output)
                res = str(pytesseract.image_to_string(Image.open(output)))
                os.remove(output)
                metadata += res

        instance.ocr_metadata = metadata
        instance.save()
