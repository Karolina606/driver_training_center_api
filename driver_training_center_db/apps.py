from django.apps import AppConfig


class TestdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'driver_training_center_db'
    verbose_name = 'driver training center db'
    label = 'db'
