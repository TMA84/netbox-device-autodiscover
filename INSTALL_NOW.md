# Install Right Now in Home Assistant! 🚀

The plugin is ready to use immediately from GitHub!

## Quick Installation Steps

### 1. Find Your NetBox Container Name

```bash
# From Home Assistant terminal/SSH
docker ps | grep netbox
```

Look for something like `addon_a0d7b954_netbox` or `878443c7-netbox`

### 2. Install the Plugin

**One-Line Install (Recommended)**

```bash
# Replace XXXXXXXX with your addon ID (e.g., 878443c7)
docker exec -it addon_XXXXXXXX_netbox uv pip install git+https://github.com/TMA84/netbox-device-autodiscover.git
```

**Or Install from Inside Container**

```bash
# Access container
docker exec -it addon_XXXXXXXX_netbox /bin/bash

# Install using uv (the package manager in this addon)
uv pip install git+https://github.com/TMA84/netbox-device-autodiscover.git

# Exit
exit
```

### 3. Run Database Migrations

**Important!** After installing, run migrations to create database tables:

```bash
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py migrate netbox_device_autodiscovery
```

You should see:
```
Running migrations:
  Applying netbox_device_autodiscovery.0001_initial... OK
```

### 4. Configure NetBox

Find your NetBox configuration file (usually `/config/configuration.py` or `/data/configuration.py`):

```bash
# Check common locations
ls -la /config/configuration.py
ls -la /data/configuration.py
ls -la /opt/netbox/netbox/netbox/configuration.py
```

Edit the configuration file and add:

```python
PLUGINS = [
    'netbox_device_autodiscovery',
]

PLUGINS_CONFIG = {
    'netbox_device_autodiscovery': {
        'snmp_community': 'public',  # Change to your SNMP community
        'enable_snmp': True,
    }
}
```

### 4. Exit and Restart

```bash
# Exit the container
exit
```

Then restart the NetBox addon from Home Assistant:
- Go to Settings → Add-ons → NetBox
- Click "Restart"

### 5. Configure the Plugin (Important!)

After restart:

1. **Log in to NetBox** as admin
2. **Go to Admin**: Click username → Admin
3. **Find "Auto-Discovery Configuration"** under "NETBOX_DEVICE_AUTODISCOVERY"
4. **Click "Add"** (or edit existing)
5. **Set at minimum**:
   - Default Site: Select an existing site
   - SNMP Community: Your SNMP community string
6. **Save**

**If you can't find the configuration interface**, see [MANUAL_MIGRATION.md](MANUAL_MIGRATION.md)

## Verify Installation

After restart, check if the plugin is installed:

```bash
docker exec -it addon_XXXXXXXX_netbox uv pip list | grep netbox-device
```

You should see `netbox-device-autodiscovery` in the list.

## Test It Out

1. Go to your NetBox web interface
2. Navigate to IPAM → IP Addresses
3. Create a new IP address (e.g., 192.168.1.1)
4. The plugin will automatically try to discover the device
5. Check Devices → Devices to see if a new device was created

## Troubleshooting

**Can't find configuration file?**
```bash
docker exec -it addon_XXXXXXXX_netbox find / -name "configuration.py" 2>/dev/null
```

**Check logs:**
```bash
docker logs -f addon_XXXXXXXX_netbox
```

**Plugin not loading?**
```bash
docker exec -it addon_XXXXXXXX_netbox python -c "from netbox_device_autodiscovery import config; print(config.name)"
```

## Configuration Options

```python
PLUGINS_CONFIG = {
    'netbox_device_autodiscovery': {
        'snmp_community': 'public',      # SNMP community string
        'snmp_version': 2,                # SNMP version (1, 2, or 3)
        'ssh_timeout': 10,                # SSH timeout in seconds
        'enable_snmp': True,              # Enable SNMP discovery
        'enable_ssh': False,              # Enable SSH discovery (future)
    }
}
```

## What Gets Created Automatically

When you create an IP address, the plugin will:

✅ Discover device via SNMP (or DNS fallback)
✅ Create Manufacturer (Cisco, Juniper, etc.)
✅ Create Device Type (from device model)
✅ Create Device Role ("Auto-Discovered")
✅ Create Site (from SNMP location or default)
✅ Create Platform (IOS, NX-OS, Junos, etc.)
✅ Create Device with all the above
✅ Create Management interface
✅ Assign the IP to the interface
✅ Discover and create additional interfaces
✅ Tag device as "auto-discovered"

## Need Help?

- Check the full documentation: [README.md](README.md)
- View detailed installation options: [INSTALL_HOME_ASSISTANT.md](INSTALL_HOME_ASSISTANT.md)
- Report issues: https://github.com/TMA84/netbox-device-autodiscover/issues
