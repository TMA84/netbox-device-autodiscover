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
        logger.debug(f"IP address {instance.address} was updated, not created. Skipping discovery.")
        return
    
    # Skip if IP already has a device assigned
    if instance.assigned_object:
        logger.info(f"IP address {instance.address} already has a device assigned. Skipping discovery.")
        return
    
    logger.info(f"🔍 NEW IP ADDRESS DETECTED: {instance.address}")
    logger.info(f"🚀 Starting automatic device discovery for {instance.address}...")
    
    try:
        discovery = DeviceDiscovery(instance)
        device = discovery.discover_and_create_device()
        
        if device:
            logger.info(f"✅ SUCCESS! Created device: {device.name} for IP {instance.address}")
            logger.info(f"   - Manufacturer: {device.device_type.manufacturer.name}")
            logger.info(f"   - Device Type: {device.device_type.model}")
            logger.info(f"   - Site: {device.site.name}")
            logger.info(f"   - Role: {device.device_role.name}")
        else:
            logger.warning(f"⚠️  Could not discover device for IP {instance.address}")
            logger.warning(f"   - Device may be unreachable or SNMP may be disabled")
    
    except Exception as e:
        logger.error(f"❌ ERROR during device discovery for IP {instance.address}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
