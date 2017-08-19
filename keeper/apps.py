from django.apps import AppConfig

from keeper.security import initialize_global_context


class KeeperConfig(AppConfig):
    name = 'keeper'

    def ready(self):
        initialize_global_context()
