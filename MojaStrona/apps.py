from django.apps import AppConfig

class MojaStronaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MojaStrona'

    def ready(self):
        import MojaStrona.signals
