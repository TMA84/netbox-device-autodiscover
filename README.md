# NetBox Device Auto-Discovery Plugin

A NetBox plugin that automatically discovers and creates devices when IP addresses are created in NetBox.

## Features

- **Automatic Device Discovery**: Triggers when a new IP address is created
- **SNMP Discovery**: Retrieves device information using SNMP (sysName, sysDescr, sysLocation, etc.)
- **Interface Discovery**: Automatically discovers and creates network interfaces
- **Smart Manufacturer Detection**: Identifies manufacturer from device information
- **Auto-creates Required Objects**: Automatically creates Manufacturer, DeviceType, DeviceRole, Site, and Platform
- **DNS Fallback**: Uses reverse DNS lookup if SNMP is unavailable
- **Tagging**: Adds 'auto-discovered' tag to all discovered devices

## Installation

1. Install the plugin:
```bash
pip install netbox-device-autodiscovery
```

2. Add the plugin to your NetBox `configuration.py`:
```python
PLUGINS = [
    'netbox_device_autodiscovery',
]

PLUGINS_CONFIG = {
    'netbox_device_autodiscovery': {
        'snmp_community': 'public',  # SNMP community string
        'snmp_version': 2,            # SNMP version (1, 2, or 3)
        'ssh_timeout': 10,            # SSH timeout in seconds
        'enable_snmp': True,          # Enable SNMP discovery
        'enable_ssh': False,          # Enable SSH discovery (future)
    }
}
```

3. Run database migrations:
```bash
cd /opt/netbox/netbox/
python3 manage.py migrate
```

4. Restart NetBox:
```bash
sudo systemctl restart netbox netbox-rq
```

## Usage

Simply create a new IP address in NetBox. The plugin will automatically:

1. Detect the new IP address creation
2. Attempt to discover the device using SNMP
3. Fall back to DNS lookup if SNMP fails
4. Create the device with all necessary information:
   - Device name (from sysName or hostname)
   - Manufacturer (detected from device description)
   - Device Type (from device model)
   - Device Role (Auto-Discovered)
   - Site (from sysLocation or default)
   - Platform (detected from OS)
   - Management interface with the IP assigned
   - Additional interfaces discovered via SNMP

## Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `snmp_community` | `'public'` | SNMP community string for device access |
| `snmp_version` | `2` | SNMP version to use (1, 2, or 3) |
| `ssh_timeout` | `10` | Timeout for SSH connections in seconds |
| `enable_snmp` | `True` | Enable SNMP-based discovery |
| `enable_ssh` | `False` | Enable SSH-based discovery (not yet implemented) |

## Requirements

- NetBox 3.0 or higher
- Python 3.8 or higher
- pysnmp >= 4.4.12
- netmiko >= 3.4.0

## How It Works

1. **Signal Trigger**: When a new IP address is created, Django's `post_save` signal triggers the discovery process
2. **SNMP Discovery**: The plugin attempts to query the device using SNMP to retrieve:
   - System name (sysName)
   - System description (sysDescr)
   - System location (sysLocation)
   - System contact (sysContact)
   - Network interfaces
3. **DNS Fallback**: If SNMP fails, the plugin performs a reverse DNS lookup
4. **Object Creation**: The plugin creates all necessary NetBox objects:
   - Manufacturer (detected or "Generic")
   - Device Type (from device model)
   - Device Role ("Auto-Discovered")
   - Site (from location or "Default Site")
   - Platform (detected from OS)
   - Device
   - Management Interface
   - Additional Interfaces
5. **IP Assignment**: The original IP address is assigned to the management interface
6. **Tagging**: An "auto-discovered" tag is added to the device

## Security Considerations

- Ensure SNMP community strings are properly secured
- Use SNMP v3 with authentication when possible
- Limit SNMP access to trusted networks
- Review auto-discovered devices before putting them into production

## Troubleshooting

Check NetBox logs for discovery information:
```bash
tail -f /opt/netbox/netbox/netbox.log
```

Look for entries with `netbox.plugins.device_autodiscovery` prefix.

## Future Enhancements

- SSH-based discovery for devices without SNMP
- LLDP/CDP neighbor discovery
- Automatic cable connections based on neighbor information
- Custom device role assignment based on device type
- Integration with external IPAM systems
- Support for SNMP v3 authentication

## License

This project is licensed under the Apache 2.0 License.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.
