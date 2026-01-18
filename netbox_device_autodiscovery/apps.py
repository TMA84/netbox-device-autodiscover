from django.apps import AppConfig


class DeviceAutoDiscoveryAppConfig(AppConfig):
    name = 'netbox_device_autodiscovery'
    verbose_name = 'Device Auto-Discovery'

    def ready(self):
        import netbox_device_autodiscovery.signals
