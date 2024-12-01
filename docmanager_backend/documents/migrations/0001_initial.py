# Generated by Django 5.1.3 on 2024-11-23 17:01

import django.utils.timezone
import documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "document_type",
                    models.CharField(
                        choices=[
                            ("pdf", "PDF"),
                            ("image", "Image"),
                            ("video", "Video"),
                            ("doc", "Word Document"),
                            ("excel", "Excel Document"),
                            ("ppt", "Powerpoint Document"),
                        ],
                        max_length=32,
                    ),
                ),
                ("number_pages", models.IntegerField()),
                (
                    "file",
                    models.FileField(upload_to=documents.models.Document.upload_to),
                ),
                (
                    "date_uploaded",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
            ],
        ),
    ]
