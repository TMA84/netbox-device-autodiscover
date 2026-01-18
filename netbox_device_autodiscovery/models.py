from django.db import models
from dcim.models import Site, DeviceRole
from tenancy.models import Tenant
from dcim.models import Location


class AutoDiscoveryConfig(models.Model):
    """
    Configuration for automatic device discovery.
    """
    # General settings
    enabled = models.BooleanField(
        default=True,
        help_text="Enable or disable automatic device discovery"
    )
    
    # SNMP settings
    snmp_enabled = models.BooleanField(
        default=True,
        help_text="Enable SNMP-based discovery"
    )
    snmp_community = models.CharField(
        max_length=100,
        default='public',
        help_text="SNMP community string for device discovery"
    )
    snmp_version = models.IntegerField(
        default=2,
        choices=[(1, 'v1'), (2, 'v2c'), (3, 'v3')],
        help_text="SNMP version to use"
    )
    snmp_timeout = models.IntegerField(
        default=5,
        help_text="SNMP timeout in seconds"
    )
    
    # DNS settings
    dns_enabled = models.BooleanField(
        default=True,
        help_text="Enable DNS fallback when SNMP fails"
    )
    
    # Default assignments
    default_site = models.ForeignKey(
        Site,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Default site for discovered devices (if not detected from SNMP location)"
    )
    default_device_role = models.ForeignKey(
        DeviceRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Default device role for discovered devices"
    )
    default_tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Default tenant for discovered devices"
    )
    default_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Default location for discovered devices"
    )
    
    # Behavior settings
    create_site_from_location = models.BooleanField(
        default=True,
        help_text="Automatically create sites from SNMP location field"
    )
    create_interfaces = models.BooleanField(
        default=True,
        help_text="Automatically discover and create interfaces"
    )
    set_primary_ip = models.BooleanField(
        default=True,
        help_text="Automatically set the discovered IP as primary IP"
    )
    
    # Naming
    device_name_template = models.CharField(
        max_length=200,
        default='{sysName}',
        help_text="Template for device names. Available variables: {sysName}, {ip}, {hostname}"
    )
    
    class Meta:
        verbose_name = "Auto-Discovery Configuration"
        verbose_name_plural = "Auto-Discovery Configuration"
    
    def __str__(self):
        return "Auto-Discovery Configuration"
    
    @classmethod
    def get_config(cls):
        """
        Get the configuration instance (singleton pattern).
        """
        config, created = cls.objects.get_or_create(pk=1)
        return config
