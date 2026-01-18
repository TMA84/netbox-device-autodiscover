import socket
from pysnmp.hlapi import *
from netmiko import ConnectHandler
from dcim.models import Device, DeviceType, DeviceRole, Site, Manufacturer, Interface, Platform
from ipam.models import IPAddress
from extras.models import Tag
from django.conf import settings
import logging
import ipaddress

logger = logging.getLogger('netbox.plugins.device_autodiscovery')


class DeviceDiscovery:
    """
    Handles device discovery using SNMP and SSH protocols.
    """
    
    def __init__(self, ip_address_obj):
        self.ip_address_obj = ip_address_obj
        self.ip = str(ip_address_obj.address.ip)
        self.config = settings.PLUGINS_CONFIG.get('netbox_device_autodiscovery', {})
        self.device_info = {}
    
    def discover_and_create_device(self):
        """
        Main method to discover device information and create the device in NetBox.
        """
        # Try to discover device information
        if self.config.get('enable_snmp', True):
            self.discover_via_snmp()
        
        if not self.device_info and self.config.get('enable_ssh', False):
            self.discover_via_ssh()
        
        # If no discovery method worked, try basic DNS/ping
        if not self.device_info:
            self.discover_basic()
        
        # Create device if we have enough information
        if self.device_info:
            return self.create_device()
        
        return None
    
    def discover_via_snmp(self):
        """
        Discover device information using SNMP.
        """
        try:
            community = self.config.get('snmp_community', 'public')
            logger.info(f"🔎 Attempting SNMP discovery for {self.ip} with community '{community}'...")
            
            # SNMP OIDs for common device information
            oids = {
                'sysName': '1.3.6.1.2.1.1.5.0',
                'sysDescr': '1.3.6.1.2.1.1.1.0',
                'sysObjectID': '1.3.6.1.2.1.1.2.0',
                'sysContact': '1.3.6.1.2.1.1.4.0',
                'sysLocation': '1.3.6.1.2.1.1.6.0',
            }
            
            for key, oid in oids.items():
                iterator = getCmd(
                    SnmpEngine(),
                    CommunityData(community),
                    UdpTransportTarget((self.ip, 161), timeout=5, retries=1),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid))
                )
                
                errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
                
                if errorIndication or errorStatus:
                    continue
                
                for varBind in varBinds:
                    self.device_info[key] = str(varBind[1])
            
            if self.device_info:
                logger.info(f"✅ SNMP discovery successful for {self.ip}")
                logger.info(f"   - System Name: {self.device_info.get('sysName', 'N/A')}")
                logger.info(f"   - Description: {self.device_info.get('sysDescr', 'N/A')[:80]}...")
                logger.info(f"   - Location: {self.device_info.get('sysLocation', 'N/A')}")
                
                # Discover interfaces
                self.discover_interfaces_snmp()
            else:
                logger.warning(f"⚠️  SNMP discovery returned no data for {self.ip}")
        
        except Exception as e:
            logger.warning(f"⚠️  SNMP discovery failed for {self.ip}: {str(e)}")
    
    def discover_interfaces_snmp(self):
        """
        Discover network interfaces using SNMP.
        """
        try:
            community = self.config.get('snmp_community', 'public')
            interfaces = []
            
            # Walk interface names (ifDescr)
            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData(community),
                UdpTransportTarget((self.ip, 161), timeout=5, retries=1),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2')),
                lexicographicMode=False
            ):
                if errorIndication or errorStatus:
                    break
                
                for varBind in varBinds:
                    interfaces.append(str(varBind[1]))
            
            self.device_info['interfaces'] = interfaces[:20]  # Limit to first 20 interfaces
        
        except Exception as e:
            logger.warning(f"Interface discovery failed for {self.ip}: {str(e)}")
    
    def discover_via_ssh(self):
        """
        Discover device information using SSH (placeholder for future implementation).
        """
        # This would require credentials management
        logger.info(f"SSH discovery not yet implemented for {self.ip}")
        pass
    
    def discover_basic(self):
        """
        Basic discovery using DNS and ping.
        """
        try:
            logger.info(f"🔎 Attempting DNS lookup for {self.ip}...")
            # Try reverse DNS lookup
            hostname = socket.gethostbyaddr(self.ip)[0]
            self.device_info['sysName'] = hostname
            logger.info(f"✅ DNS lookup successful: {hostname}")
        except socket.herror:
            # Use IP as hostname if DNS fails
            self.device_info['sysName'] = f"device-{self.ip.replace('.', '-')}"
            logger.info(f"⚠️  No DNS record found, using generated name: {self.device_info['sysName']}")
    
    def create_device(self):
        """
        Create device and related objects in NetBox.
        """
        try:
            logger.info(f"📝 Creating device in NetBox...")
            
            # Get or create manufacturer
            manufacturer = self.get_or_create_manufacturer()
            logger.info(f"   ✓ Manufacturer: {manufacturer.name}")
            
            # Get or create device type
            device_type = self.get_or_create_device_type(manufacturer)
            logger.info(f"   ✓ Device Type: {device_type.model}")
            
            # Get or create device role
            device_role = self.get_or_create_device_role()
            logger.info(f"   ✓ Device Role: {device_role.name}")
            
            # Get or create site
            site = self.get_or_create_site()
            logger.info(f"   ✓ Site: {site.name}")
            
            # Get or create platform
            platform = self.get_or_create_platform()
            if platform:
                logger.info(f"   ✓ Platform: {platform.name}")
            
            # Create device name
            device_name = self.device_info.get('sysName', f"device-{self.ip.replace('.', '-')}")
            
            # Check if device already exists
            existing_device = Device.objects.filter(name=device_name).first()
            if existing_device:
                logger.info(f"ℹ️  Device {device_name} already exists, skipping creation")
                return existing_device
            
            # Create device
            device = Device.objects.create(
                name=device_name,
                device_type=device_type,
                device_role=device_role,
                site=site,
                platform=platform,
                comments=f"Auto-discovered from IP {self.ip}\n{self.device_info.get('sysDescr', '')}"
            )
            logger.info(f"   ✓ Device created: {device.name}")
            
            # Create management interface
            self.create_management_interface(device)
            logger.info(f"   ✓ Management interface created")
            
            # Create additional interfaces
            interface_count = len(self.device_info.get('interfaces', []))
            if interface_count > 0:
                self.create_interfaces(device)
                logger.info(f"   ✓ Created {interface_count} additional interfaces")
            
            # Add auto-discovery tag
            tag, _ = Tag.objects.get_or_create(
                name='auto-discovered',
                defaults={'color': '4caf50', 'description': 'Automatically discovered device'}
            )
            device.tags.add(tag)
            logger.info(f"   ✓ Tagged as 'auto-discovered'")
            
            logger.info(f"✅ Device creation complete: {device.name}")
            return device
        
        except Exception as e:
            logger.error(f"❌ Error creating device: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    
    def get_or_create_manufacturer(self):
        """
        Extract and create manufacturer from device info.
        """
        # Try to parse manufacturer from sysDescr or sysObjectID
        sys_descr = self.device_info.get('sysDescr', '').lower()
        
        manufacturer_map = {
            'cisco': 'Cisco',
            'juniper': 'Juniper',
            'arista': 'Arista',
            'hp': 'HP',
            'dell': 'Dell',
            'huawei': 'Huawei',
            'mikrotik': 'MikroTik',
            'ubiquiti': 'Ubiquiti',
            'fortinet': 'Fortinet',
            'palo alto': 'Palo Alto Networks',
        }
        
        manufacturer_name = 'Generic'
        for key, value in manufacturer_map.items():
            if key in sys_descr:
                manufacturer_name = value
                break
        
        manufacturer, created = Manufacturer.objects.get_or_create(
            name=manufacturer_name,
            defaults={'slug': manufacturer_name.lower().replace(' ', '-')}
        )
        
        if created:
            logger.info(f"Created manufacturer: {manufacturer_name}")
        
        return manufacturer
    
    def get_or_create_device_type(self, manufacturer):
        """
        Create device type based on discovered information.
        """
        sys_descr = self.device_info.get('sysDescr', 'Unknown Device')
        
        # Create a simplified model name
        model = sys_descr[:50] if len(sys_descr) > 50 else sys_descr
        model = model.replace('/', '-').replace(' ', '-')
        
        device_type, created = DeviceType.objects.get_or_create(
            manufacturer=manufacturer,
            model=model,
            defaults={
                'slug': f"{manufacturer.slug}-{model[:40]}".lower().replace(' ', '-')[:50],
            }
        )
        
        if created:
            logger.info(f"Created device type: {model}")
        
        return device_type
    
    def get_or_create_device_role(self):
        """
        Get or create a default device role.
        """
        device_role, created = DeviceRole.objects.get_or_create(
            name='Auto-Discovered',
            defaults={
                'slug': 'auto-discovered',
                'color': '2196f3',
                'vm_role': False
            }
        )
        
        if created:
            logger.info("Created device role: Auto-Discovered")
        
        return device_role
    
    def get_or_create_site(self):
        """
        Get or create site based on IP location or default.
        """
        location = self.device_info.get('sysLocation', '').strip()
        
        if location:
            site_name = location[:50]
            slug = location[:50].lower().replace(' ', '-')
        else:
            site_name = 'Default Site'
            slug = 'default-site'
        
        site, created = Site.objects.get_or_create(
            slug=slug,
            defaults={'name': site_name}
        )
        
        if created:
            logger.info(f"Created site: {site_name}")
        
        return site
    
    def get_or_create_platform(self):
        """
        Determine and create platform based on device info.
        """
        sys_descr = self.device_info.get('sysDescr', '').lower()
        
        platform_map = {
            'ios': 'Cisco IOS',
            'nxos': 'Cisco NX-OS',
            'junos': 'Juniper Junos',
            'eos': 'Arista EOS',
            'routeros': 'MikroTik RouterOS',
        }
        
        platform_name = None
        for key, value in platform_map.items():
            if key in sys_descr:
                platform_name = value
                break
        
        if not platform_name:
            return None
        
        platform, created = Platform.objects.get_or_create(
            name=platform_name,
            defaults={'slug': platform_name.lower().replace(' ', '-')}
        )
        
        if created:
            logger.info(f"Created platform: {platform_name}")
        
        return platform
    
    def create_management_interface(self, device):
        """
        Create management interface and assign the IP address.
        """
        try:
            interface, created = Interface.objects.get_or_create(
                device=device,
                name='Management',
                defaults={
                    'type': 'virtual',
                    'mgmt_only': True
                }
            )
            
            # Assign IP address to interface
            self.ip_address_obj.assigned_object = interface
            self.ip_address_obj.save()
            
            # Set as primary IP if not already set
            if not device.primary_ip4 and self.ip_address_obj.family == 4:
                device.primary_ip4 = self.ip_address_obj
                device.save()
            elif not device.primary_ip6 and self.ip_address_obj.family == 6:
                device.primary_ip6 = self.ip_address_obj
                device.save()
            
            logger.info(f"Created management interface for device {device.name}")
        
        except Exception as e:
            logger.error(f"Error creating management interface: {str(e)}")
    
    def create_interfaces(self, device):
        """
        Create additional interfaces discovered via SNMP.
        """
        interfaces = self.device_info.get('interfaces', [])
        
        for idx, interface_name in enumerate(interfaces):
            try:
                # Skip if interface already exists
                if Interface.objects.filter(device=device, name=interface_name).exists():
                    continue
                
                # Determine interface type
                interface_type = self.determine_interface_type(interface_name)
                
                Interface.objects.create(
                    device=device,
                    name=interface_name,
                    type=interface_type,
                    enabled=True
                )
            
            except Exception as e:
                logger.warning(f"Error creating interface {interface_name}: {str(e)}")
    
    def determine_interface_type(self, interface_name):
        """
        Determine interface type based on name.
        """
        name_lower = interface_name.lower()
        
        if 'ethernet' in name_lower or 'eth' in name_lower:
            return '1000base-t'
        elif 'gigabit' in name_lower or 'ge' in name_lower:
            return '1000base-t'
        elif 'fastethernet' in name_lower or 'fa' in name_lower:
            return '100base-tx'
        elif 'tengigabit' in name_lower or 'te' in name_lower:
            return '10gbase-x-sfpp'
        elif 'serial' in name_lower:
            return 'other'
        elif 'loopback' in name_lower or 'lo' in name_lower:
            return 'virtual'
        else:
            return 'other'
