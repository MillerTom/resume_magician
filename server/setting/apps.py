from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_entry(sender, **kwargs):
    from setting.models import DataSource, SupervisorStatus

    if not DataSource.objects.exists():
        DataSource.objects.create(value='database')

    if not SupervisorStatus.objects.exists():
        SupervisorStatus.objects.create(is_locked=False)    


class SettingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'setting'

    def ready(self):
        post_migrate.connect(create_default_entry, sender=self)