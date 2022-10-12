from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auser'

    def ready(self):
        ''' Create roles if not exist after migration '''
        from auser.signals import create_role
        post_migrate.connect(create_role, self)