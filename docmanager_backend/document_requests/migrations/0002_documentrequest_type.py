# Generated by Django 5.1.3 on 2024-11-24 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("document_requests", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="documentrequest",
            name="type",
            field=models.CharField(
                choices=[("softcopy", "Softcopy"), ("hardcopy", "Hardcopy")],
                default="softcopy",
                max_length=16,
            ),
        ),
    ]
