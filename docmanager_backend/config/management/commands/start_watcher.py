from ollama import ChatResponse
import base64
import httpx
from django.core.management.base import BaseCommand

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
from config.settings import get_secret
from django.core.files import File
import logging
import time
from ollama import Client


class PDFHandler(FileSystemEventHandler):
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting Document Watcher...")

    def on_created(self, event):
        if event.is_directory:
            return None

        if event.src_path.endswith(".pdf"):
            self.logger.info(f"New PDF file detected: {event.src_path}")
            self.process_pdf(event.src_path)

    def process_pdf(self, file_path):
        try:
            # Get the original filename and directory
            original_filename = os.path.basename(file_path)
            original_dir = os.path.dirname(file_path)

            # Check if the filename contains spaces
            if " " in original_filename:
                # Create the new filename by replacing spaces
                new_filename = original_filename.replace(" ", "_")

                # Construct the new full file path
                new_file_path = os.path.join(original_dir, new_filename)

                # Rename the file
                os.rename(file_path, new_file_path)

                # Update the filename and file_path variables
                filename = new_filename
                file_path = new_file_path
            else:
                filename = original_filename
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

                    # Get document category
                    # Try to pass image to the Ollama image recognition API first
                    try:
                        client = Client(
                            host=get_secret("OLLAMA_URL"),
                            auth=httpx.BasicAuth(
                                username=get_secret("OLLAMA_USERNAME"), password=get_secret("OLLAMA_PASSWORD")) if get_secret("OLLAMA_USE_AUTH") else None
                        )

                        encoded_image = base64.b64encode(
                            img_buffer.getvalue()).decode()

                        attempts = 0
                        while True:
                            if attempts >= 3:
                                raise Exception(
                                    "Unable to categorize using Ollama API")
                            attempts += 1

                            content = f"""
                            Read the text from the image and provide a category.

                            Possible categories are: Announcement, Manual, Form

                            Respond only with the category. No explanations are necessary.
                            """

                            response: ChatResponse = client.chat(
                                model=get_secret("OLLAMA_MODEL"),
                                messages=[
                                    {"role": "user", "content": content,
                                        "images": [encoded_image]},
                                ],
                            )

                            document_type = response["message"]["content"].replace(
                                "*", "").replace(".", "")

                            # A few safety checks if the model does not follow through with output instructions
                            if len(document_type) > 16:
                                self.logger.warning(
                                    f"Ollama API gave incorrect document category: {response['message']['content']}. Retrying...")
                            break

                    # If that fails, just use regular OCR read the title as a dirty fix/fallback
                    except Exception as e:
                        self.logger.warning(f"Error! {e}")
                        self.logger.warning(
                            "Ollama OCR offloading failed. Falling back to default OCR")
                        lines = text.split("\n")

                        for line in lines:
                            if line.strip():
                                document_type = line.strip().lower()
                                break

                        if not document_type:
                            document_type = "other"

                    metadata += text

            # Open the file for instance creation
            DOCUMENT, created = Document.objects.get_or_create(
                name=filename.replace(".pdf", ""),
                defaults={
                    "number_pages": num_pages,
                    "ocr_metadata": metadata,
                    "document_type": document_type,
                },
            )

            if created:
                DOCUMENT.file.save(
                    name=filename, content=File(open(file_path, "rb")))
                self.logger.info(
                    f"Document '{filename}' created successfully with type '{document_type}'."
                )

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
        watch_directory = os.path.join(MEDIA_ROOT, "uploads")

        self.observer.schedule(event_handler, watch_directory, recursive=True)
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
