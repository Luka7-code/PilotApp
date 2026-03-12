from django.apps import AppConfig
import threading


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        from home.views import poll_opensky
        
        thread = threading.Thread(target=poll_opensky, daemon=True)
        thread.start()