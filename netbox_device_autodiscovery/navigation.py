from extras.plugins import PluginMenuButton, PluginMenuItem

menu_items = (
    PluginMenuItem(
        link='admin:netbox_device_autodiscovery_autodiscoveryconfig_changelist',
        link_text='Auto-Discovery Settings',
        permissions=['netbox_device_autodiscovery.view_autodiscoveryconfig'],
        buttons=()
    ),
)
