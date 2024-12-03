from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "documents"

    def ready(self) -> None:
        import documents.signals

        return super().ready()
