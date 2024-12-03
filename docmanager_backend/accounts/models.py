from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now, localdate


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

    role = models.CharField(
        max_length=32, choices=ROLE_CHOICES, default="client")

    date_joined = models.DateTimeField(default=now, editable=False)

    SEX_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    sex = models.CharField(
        max_length=32, choices=SEX_CHOICES, blank=False, null=False)
    birthday = models.DateField(blank=False, null=False)

    @property
    def age(self):
        date_now = localdate(now())
        age = (
            date_now.year
            - self.birthday.year
            - (
                (date_now.month, date_now.day)
                < (self.birthday.month, self.birthday.day)
            )
        )
        return age

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, **kwargs):
        self.username = self.email
        super().save(**kwargs)
