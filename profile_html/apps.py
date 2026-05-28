from django.apps import AppConfig

class ProfileHtmlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile_html'

    def ready(self):
        # Waxaan u sheegaynaa abka marka uu kacyo inuu roro signals-ka rasmiga ah
        import profile_html.signals