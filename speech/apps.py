from django.apps import AppConfig


class SpeechConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'speech'

    def ready(self):
        from jobs import updater
        updater.start()
