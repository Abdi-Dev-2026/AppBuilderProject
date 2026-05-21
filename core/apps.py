from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Waxaa la saxay indention-ka (4 spaces) si looga fogaado IndentationError
        import core.signals