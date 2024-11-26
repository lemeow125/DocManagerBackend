from django.core.management.base import BaseCommand, CommandError

from io import BytesIO
from documents.models import Document
from PIL import Image
import pytesseract
import fitz
import os
from config.settings import MEDIA_ROOT
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from documents.models import Document
import logging
import time


class PDFHandler(FileSystemEventHandler):
    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting Document Watcher...")

    def on_created(self, event):
        if event.is_directory:
            return None

        if event.src_path.endswith('.pdf'):
            self.logger.info(f"New PDF file detected: {event.src_path}")
            self.process_pdf(event.src_path)

    def process_pdf(self, file_path):
        try:
            filename = os.path.basename(file_path)
            metadata = ""
            document_type = ""

            with fitz.open(file_path) as doc:
                num_pages = len(doc)

                for page_num in range(num_pages):
                    page = doc[page_num]
                    pix = page.get_pixmap(matrix=(1.2, 1.2))

                    # Convert pixmap to bytes
                    img_bytes = pix.tobytes()

                    # Create a BytesIO object
                    img_buffer = BytesIO(img_bytes)

                    # Create a PIL Image object from the bytes
                    img = Image.open(img_buffer)

                    # Perform OCR
                    text = pytesseract.image_to_string(img).strip()

                    lines = text.split('\n')

                    for line in lines:
                        if line.strip():
                            document_type = line.strip().lower()
                            break
                    if not document_type or document_type not in Document.DOCUMENT_TYPE_CHOICES:
                        document_type = "other"

                    metadata += text

            document, created = Document.objects.get_or_create(
                name=filename,
                defaults={
                    'number_pages': num_pages,
                    'ocr_metadata': metadata,
                    'document_type': document_type
                }
            )

            if created:
                self.logger.info(f"Document '{filename}' created successfully with type '{
                    document_type}'.")

            else:
                self.logger.info(f"Document '{filename}' already exists.")

            os.remove(file_path)
        except Exception as e:
            self.logger.error(f"Error processing PDF: {str(e)}")


class PDFWatcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = PDFHandler()
        watch_directory = f"{MEDIA_ROOT}/uploads"

        self.observer.schedule(
            event_handler, watch_directory, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()

        self.observer.join()


class Command(BaseCommand):
    help = "Runs a dedicated file watcher service"

    def handle(self, *args, **options):
        watcher = PDFWatcher()
        watcher.run()
