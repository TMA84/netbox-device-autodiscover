from django.apps import AppConfig


class DeviceAutoDiscoveryAppConfig(AppConfig):
    name = 'netbox_device_autodiscovery'
    verbose_name = 'Device Auto-Discovery'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import netbox_device_autodiscovery.signals
