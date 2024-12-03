from config.settings import get_secret
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.timezone import now, localdate

from .models import CustomUser


@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    # Programatically creates the administrator account
    if sender.name == "accounts":
        ADMIN_USER = CustomUser.objects.filter(
            email=get_secret("ADMIN_EMAIL")).first()
        if not ADMIN_USER:
            ADMIN_USER = CustomUser.objects.create_superuser(
                username=get_secret("ADMIN_EMAIL"),
                email=get_secret("ADMIN_EMAIL"),
                password=get_secret("ADMIN_PASSWORD"),
                sex="male",
                birthday=localdate(now()),
            )

            print("Created administrator account:", ADMIN_USER.email)

            ADMIN_USER.first_name = "Administrator"
            ADMIN_USER.is_active = True
            ADMIN_USER.save()
