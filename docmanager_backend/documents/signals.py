from io import BytesIO
from documents.models import Document
from django.db.models.signals import post_save
from django.dispatch import receiver
from config.settings import MEDIA_ROOT
import os
import fitz
import pytesseract
from PIL import Image
from .models import Document


@receiver(post_save, sender=Document)
def document_post_save(sender, instance, **kwargs):
    if not instance.ocr_metadata:
        metadata = ""
        with fitz.open(os.path.join(MEDIA_ROOT, instance.file.name)) as doc:
            mat = fitz.Matrix(1.2, 1.2)
            for page in doc:
                pix = page.get_pixmap(matrix=mat)
                # Convert pixmap to bytes
                img_bytes = pix.tobytes()

                # Create a BytesIO object
                img_buffer = BytesIO(img_bytes)

                # Create a PIL Image object from the bytes
                img = Image.open(img_buffer)

                # Perform OCR
                text = pytesseract.image_to_string(img).strip()
                metadata += text

        instance.ocr_metadata = metadata
        instance.save()
