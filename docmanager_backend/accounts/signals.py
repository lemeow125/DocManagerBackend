from config.settings import get_secret
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils.timezone import now, localdate

from .models import CustomUser


@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    # Programatically creates the administrator account
    if sender.name == "accounts":
        users = [{
            "email": get_secret("ADMIN_EMAIL"),
            "role": "head",
            "admin": True,
        }, {
            "email": "staff@test.com",
            "role": "staff",
            "admin": False,
        }, {
            "email": "planning@test.com",
            "role": "planning",
            "admin": False,
        }, {
            "email": "client@test.com",
            "role": "client",
            "admin": False,
        },]
        for user in users:
            USER = CustomUser.objects.filter(
                email=user["email"]).first()
            if not USER:
                if user["admin"]:
                    USER = CustomUser.objects.create_superuser(
                        username=user["email"],
                        email=user["email"],
                        password=get_secret("ADMIN_PASSWORD"),
                        sex="male",
                        birthday=localdate(now()),
                        role=user["role"]
                    )
                else:
                    USER = CustomUser.objects.create_user(
                        username=user["email"],
                        email=user["email"],
                        password=get_secret("ADMIN_PASSWORD"),
                        sex="male",
                        birthday=localdate(now()),
                        role=user["role"]

                    )
                print(f"Created {user['role']} account: {USER.email}")

                USER.first_name = f"DEBUG_USER:{USER.email}"
                USER.is_active = True
                USER.save()
