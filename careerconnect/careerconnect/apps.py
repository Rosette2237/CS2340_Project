from django.apps import AppConfig

class CareerconnectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'careerconnect'

    def ready(self):
        import careerconnect.admin_extensions  # loads User/Group overrides