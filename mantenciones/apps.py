from django.apps import AppConfig

class MantencionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mantenciones'

    def ready(self):
        import mantenciones.signals  # activa señales