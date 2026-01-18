from netbox.plugins import PluginConfig


class DeviceAutoDiscoveryConfig(PluginConfig):
    name = 'netbox_device_autodiscovery'
    verbose_name = 'Device Auto-Discovery'
    description = 'Automatically discovers and creates devices when IP addresses are created'
    version = '1.0.0'
    author = 'NetBox Plugin'
    author_email = 'plugin@example.com'
    base_url = 'device-autodiscovery'
    required_settings = []
    default_settings = {
        'snmp_community': 'public',
        'snmp_version': 2,
        'ssh_timeout': 10,
        'enable_snmp': True,
        'enable_ssh': False,
    }
    
    def ready(self):
        super().ready()
        import netbox_device_autodiscovery.signals


config = DeviceAutoDiscoveryConfig
