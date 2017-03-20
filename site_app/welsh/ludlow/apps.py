from django.apps import AppConfig


class LudlowConfig(AppConfig):
    name = 'welsh.ludlow'

    def ready(self):
        from . import signals
