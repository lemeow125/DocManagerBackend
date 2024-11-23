from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class CustomUser(AbstractUser):
    # first_name inherited from base user class
    # last_name inherited from base user class
    # username inherited from base user class
    # password inherited from base user class
    # is_admin inherited from base user class

    email = models.EmailField(blank=False, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    ROLE_CHOICES = (
        ("head", "Head"),
        ("admin", "Admin"),
        ("client", "Client"),
        ("planning", "Planning"),
        ("staff", "Staff"),
    )

    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default="client")

    date_joined = models.DateTimeField(default=now, editable=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, **kwargs):
        self.username = self.email
        if self.is_staff:
            self.role = "staff"
        elif self.is_superuser:
            self.role = "admin"
        super().save(**kwargs)
