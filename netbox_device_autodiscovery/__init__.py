from netbox.plugins import PluginConfig


class DeviceAutoDiscoveryConfig(PluginConfig):
    name = 'netbox_device_autodiscovery'
    verbose_name = 'Device Auto-Discovery'
    description = 'Automatically discovers and creates devices when IP addresses are created'
    version = '1.0.0'
    author = 'NetBox Plugin'
    author_email = '[email]'
    base_url = 'device-autodiscovery'
    required_settings = []
    default_settings = {
        'snmp_community': 'public',
        'snmp_version': 2,
        'ssh_timeout': 10,
        'enable_snmp': True,
        'enable_ssh': False,
    }


config = DeviceAutoDiscoveryConfig
