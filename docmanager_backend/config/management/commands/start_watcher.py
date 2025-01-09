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
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
import calendar


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

                # Perform OCR only on the first page
                page = doc[0]
                pix = page.get_pixmap(matrix=(1.2, 1.2))

                # Convert pixmap to bytes
                img_bytes = pix.tobytes()

                # Create a BytesIO object
                img_buffer = BytesIO(img_bytes)

                # Create a PIL Image object from the bytes
                img = Image.open(img_buffer)

                # Perform OCR
                text = pytesseract.image_to_string(img).strip()

                # Try to pass image to the Ollama image recognition API first
                try:
                    client = Client(
                        host=get_secret("OLLAMA_URL"),
                        auth=httpx.BasicAuth(
                            username=get_secret("OLLAMA_USERNAME"), password=get_secret("OLLAMA_PASSWORD")) if get_secret("OLLAMA_USE_AUTH") else None,
                    )

                    encoded_image = base64.b64encode(
                        img_buffer.getvalue()).decode()

                    # Determine category
                    class DocumentSchema(BaseModel):
                        category: str = "other"
                        explanation: Optional[str] = None

                    possible_categories = set((Document.objects.all().values_list(
                        "document_type", flat=True), "Documented Procedures Manual", "Form", "Special Order", "Memorandum"))
                    prompt = f"""
                        Read the text from the image and provide a document_type.

                        Possible document types are: {possible_categories}. You are free to create a new one if none are suitable.

                        Do all of this and return your output in JSON.
                        """

                    response = client.chat(
                        model=get_secret("OLLAMA_MODEL"),
                        messages=[
                            {"role": "user",
                                "content": prompt,
                                "images": [encoded_image]},
                        ],
                        format=DocumentSchema.model_json_schema(),
                        options={
                            "temperature": 0
                        },
                    )
                    result = DocumentSchema.model_validate_json(
                        response.message.content)
                    document_type = result.category

                    # Determine sender
                    class DocumentSchema(BaseModel):
                        sent_from: str = "N/A"
                        explanation: Optional[str] = None

                    prompt = f"""
                        Determine who sent the document. Otherwise, return N/A.

                        Do all of this and return your output in JSON.
                        """
                    response = client.chat(
                        model=get_secret("OLLAMA_MODEL"),
                        messages=[
                            {"role": "user",
                                "content": prompt,
                                "images": [encoded_image]},
                        ],
                        format=DocumentSchema.model_json_schema(),
                        options={
                            "temperature": 0
                        },
                    )
                    result = DocumentSchema.model_validate_json(
                        response.message.content)

                    sent_from = result.sent_from

                    # Determine subject
                    class DocumentSchema(BaseModel):
                        subject: str = "N/A"
                        explanation: Optional[str] = None

                    prompt = f"""
                        Identify the subject of the document if it exists.

                        Do all of this and return your output in JSON.
                        """
                    response = client.chat(
                        model=get_secret("OLLAMA_MODEL"),
                        messages=[
                            {"role": "user",
                                "content": prompt,
                                "images": [encoded_image]},
                        ],
                        format=DocumentSchema.model_json_schema(),
                        options={
                            "temperature": 0
                        },
                    )
                    result = DocumentSchema.model_validate_json(
                        response.message.content)

                    document_subject = result.subject

                    # Determine date
                    class DocumentSchema(BaseModel):
                        document_date: Optional[date]
                        explanation: Optional[str] = None

                    prompt = f"""
                        Identify the date of the document if it exists.

                        If you are unable to determine the date, return nothing.

                        Do all of this and return your output in JSON.
                        """
                    response = client.chat(
                        model=get_secret("OLLAMA_MODEL"),
                        messages=[
                            {"role": "user",
                                "content": prompt,
                                "images": [encoded_image]},
                        ],
                        format=DocumentSchema.model_json_schema(),
                        options={
                            "temperature": 0
                        },
                    )
                    result = DocumentSchema.model_validate_json(
                        response.message.content)

                    document_date = result.document_date

                    if document_date:
                        document_month = document_date.strftime("%B")
                        document_year = result.document_date.year
                        # Set as none for invalid dates
                        if document_year < 1980:
                            document_month = "no_month"
                            document_year = "no_year"
                    else:
                        document_month = "no_month"
                        document_year = "no_year"

                # If that fails, just use regular OCR read the title as a dirty fix/fallback
                except Exception as e:
                    document_type = "other"
                    sent_from = "N/A"
                    document_month = "no_month"
                    document_year = "no_year"

                    self.logger.warning(f"Error! {e}")
                    self.logger.warning(
                        "Ollama OCR offload failed. Using defaults for missing values")

                metadata += text

            # Open the file for instance creation
            DOCUMENT = Document.objects.filter(
                name=filename.replace(".pdf", "")).first()
            if not DOCUMENT:
                DOCUMENT = Document.objects.create(
                    name=filename.replace(".pdf", ""),
                    number_pages=num_pages,
                    ocr_metadata=metadata,
                    document_type=document_type,
                    sent_from=sent_from,
                    document_month=document_month,
                    document_year=document_year,
                    subject=document_subject
                )

                DOCUMENT.file.save(
                    name=filename, content=File(open(file_path, "rb")))

                self.logger.info(
                    f"Document '{filename}' created successfully with type '{
                        document_type}'. sent_from: {sent_from}, document_month: {document_month}, document_year: {document_year}"
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
