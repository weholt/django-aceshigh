from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


class AceshighConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aceshigh"

    def ready(self):
        from . import signals

        User = get_user_model()
        post_save.connect(signals.create_or_update_user_profile, sender=User)
