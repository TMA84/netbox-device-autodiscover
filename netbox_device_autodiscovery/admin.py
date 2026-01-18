from django.contrib import admin
from .models import AutoDiscoveryConfig


@admin.register(AutoDiscoveryConfig)
class AutoDiscoveryConfigAdmin(admin.ModelAdmin):
    """
    Admin interface for Auto-Discovery Configuration.
    """
    fieldsets = (
        ('General Settings', {
            'fields': ('enabled',)
        }),
        ('SNMP Settings', {
            'fields': ('snmp_enabled', 'snmp_community', 'snmp_version', 'snmp_timeout'),
            'description': 'Configure SNMP discovery settings'
        }),
        ('DNS Settings', {
            'fields': ('dns_enabled',),
            'description': 'DNS fallback when SNMP fails'
        }),
        ('Default Assignments', {
            'fields': ('default_site', 'default_device_role', 'default_tenant', 'default_location'),
            'description': 'Default values for discovered devices'
        }),
        ('Behavior', {
            'fields': ('create_site_from_location', 'create_interfaces', 'set_primary_ip'),
            'description': 'Control automatic creation behavior'
        }),
        ('Naming', {
            'fields': ('device_name_template',),
            'description': 'Template for device names. Available: {sysName}, {ip}, {hostname}'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one configuration instance
        return not AutoDiscoveryConfig.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of the configuration
        return False
