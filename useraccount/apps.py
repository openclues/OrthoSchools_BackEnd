from django.apps import AppConfig, apps
from django.db.models.signals import post_migrate


class UseraccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'useraccount'

    def callonread(self):
        from actstream.registry import registry
        registry.register(apps.get_model('useraccount', 'UserAccount'))
        registry.register(apps.get_model('space', 'Space'))

    def ready(self):
        import core.signals

        self.callonread()

        # Importing within the ready method to avoid import issues
        # from core.signals import add_premium_users_to_space  # Import your signal
        #
        # # Registering models with actstream
        # Space = apps.get_model('space', 'Space')
        # # registry = apps.get_app_config('actstream').registry
        # # registry.register(self.get_model('UserAccount'))
        #
        # # Connecting signals
        # post_migrate.connect(add_premium_users_to_space, sender=self)
