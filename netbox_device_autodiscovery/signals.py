from django.db.models.signals import post_save
from django.dispatch import receiver
from ipam.models import IPAddress
from dcim.models import Device, DeviceType, DeviceRole, Site, Manufacturer, Interface
from extras.models import Tag
from .discovery import DeviceDiscovery
import logging

logger = logging.getLogger('netbox.plugins.device_autodiscovery')


@receiver(post_save, sender=IPAddress)
def auto_discover_device(sender, instance, created, **kwargs):
    """
    Signal handler that triggers device discovery when a new IP address is created.
    """
    if not created:
        return
    
    # Skip if IP already has a device assigned
    if instance.assigned_object:
        return
    
    logger.info(f"New IP address created: {instance.address}. Starting device discovery...")
    
    try:
        discovery = DeviceDiscovery(instance)
        device = discovery.discover_and_create_device()
        
        if device:
            logger.info(f"Successfully created device: {device.name} for IP {instance.address}")
        else:
            logger.warning(f"Could not discover device for IP {instance.address}")
    
    except Exception as e:
        logger.error(f"Error during device discovery for IP {instance.address}: {str(e)}")
