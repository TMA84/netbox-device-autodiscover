# Testing Guide - NetBox Device Auto-Discovery

This guide shows you how to verify the plugin is working and see what it's doing.

## 1. Check Plugin is Installed

### From Home Assistant Terminal:

```bash
# Check if plugin is installed
docker exec -it addon_XXXXXXXX_netbox /opt/netbox/.venv/bin/pip list | grep netbox-device

# Should show:
# netbox-device-autodiscovery    1.0.0
```

### From NetBox Web UI:

1. Go to NetBox → Admin → Plugins
2. You should see "Device Auto-Discovery" listed

## 2. Check Plugin is Loaded

### View NetBox Logs:

```bash
# Watch logs in real-time
docker logs -f addon_XXXXXXXX_netbox

# Or check recent logs
docker logs --tail 100 addon_XXXXXXXX_netbox
```

Look for startup messages like:
```
Info: Configuring Device Auto-Discovery Plugin..
```

## 3. Test the Plugin

### Method 1: Create an IP Address in NetBox

1. **Go to NetBox Web UI**
   - Navigate to: IPAM → IP Addresses
   - Click "Add" button

2. **Create a New IP Address**
   - Address: Enter an IP (e.g., `192.168.1.1/24`)
   - Status: Active
   - Click "Create"

3. **Watch the Logs**
   ```bash
   docker logs -f addon_XXXXXXXX_netbox
   ```

4. **Look for Discovery Messages:**
   ```
   🔍 NEW IP ADDRESS DETECTED: 192.168.1.1/24
   🚀 Starting automatic device discovery for 192.168.1.1...
   🔎 Attempting SNMP discovery for 192.168.1.1 with community 'public'...
   ✅ SNMP discovery successful for 192.168.1.1
      - System Name: router-01
      - Description: Cisco IOS Software...
      - Location: Server Room
   📝 Creating device in NetBox...
      ✓ Manufacturer: Cisco
      ✓ Device Type: Cisco IOS Router
      ✓ Device Role: Auto-Discovered
      ✓ Site: Server Room
      ✓ Platform: Cisco IOS
      ✓ Device created: router-01
      ✓ Management interface created
      ✓ Created 5 additional interfaces
      ✓ Tagged as 'auto-discovered'
   ✅ SUCCESS! Created device: router-01 for IP 192.168.1.1/24
   ```

5. **Check NetBox for the New Device**
   - Go to: Devices → Devices
   - You should see the newly created device
   - It will have a green "auto-discovered" tag

### Method 2: Test with a Known Device

If you have a device with SNMP enabled:

1. **Enable SNMP on a device** (if not already enabled)
   - Community string: `public` (or configure in addon options)
   - Allow SNMP from NetBox container IP

2. **Create IP address in NetBox** for that device

3. **Watch the magic happen** in the logs!

### Method 3: Test with DNS Only (No SNMP)

1. **Create an IP address** for a device without SNMP
2. **The plugin will fall back to DNS:**
   ```
   🔎 Attempting DNS lookup for 192.168.1.100...
   ✅ DNS lookup successful: my-server.local
   ```

## 4. What to Look For

### Success Indicators:

✅ **In Logs:**
- `🔍 NEW IP ADDRESS DETECTED`
- `✅ SNMP discovery successful` or `✅ DNS lookup successful`
- `✅ SUCCESS! Created device`

✅ **In NetBox UI:**
- New device appears in Devices list
- Device has "auto-discovered" tag (green)
- Device has manufacturer, type, site, etc.
- IP is assigned to management interface
- Additional interfaces are created

### If Nothing Happens:

❌ **Check these:**

1. **Plugin not loaded?**
   ```bash
   docker exec -it addon_XXXXXXXX_netbox /opt/netbox/.venv/bin/python -c "import netbox_device_autodiscovery; print('Plugin loaded!')"
   ```

2. **Configuration missing?**
   ```bash
   docker exec -it addon_XXXXXXXX_netbox cat /opt/netbox/netbox/netbox/configuration.py | grep -A 10 "Device Auto-Discovery"
   ```
   
   Should show:
   ```python
   # Device Auto-Discovery Plugin
   PLUGINS = ['netbox_device_autodiscovery']
   PLUGINS_CONFIG = {
       'netbox_device_autodiscovery': {
           'snmp_community': 'public',
           'enable_snmp': True,
       }
   }
   ```

3. **Check for errors:**
   ```bash
   docker logs addon_XXXXXXXX_netbox 2>&1 | grep -i error
   ```

## 5. Common Log Messages

### Normal Operation:

```
🔍 NEW IP ADDRESS DETECTED: 192.168.1.1/24
🚀 Starting automatic device discovery...
🔎 Attempting SNMP discovery...
✅ SNMP discovery successful
📝 Creating device in NetBox...
✅ SUCCESS! Created device: router-01
```

### SNMP Failed, DNS Fallback:

```
🔍 NEW IP ADDRESS DETECTED: 192.168.1.100/24
🚀 Starting automatic device discovery...
🔎 Attempting SNMP discovery...
⚠️  SNMP discovery failed: Timeout
🔎 Attempting DNS lookup...
✅ DNS lookup successful: server.local
📝 Creating device in NetBox...
✅ SUCCESS! Created device: server.local
```

### Device Already Exists:

```
🔍 NEW IP ADDRESS DETECTED: 192.168.1.1/24
🚀 Starting automatic device discovery...
ℹ️  Device router-01 already exists, skipping creation
```

### IP Already Assigned:

```
IP address 192.168.1.1/24 already has a device assigned. Skipping discovery.
```

## 6. Troubleshooting

### Enable Debug Mode

In Home Assistant addon options, set:
```yaml
debug: true
```

This creates `/config/configuration-merged.py` showing the full NetBox config.

### Check SNMP Connectivity

From inside the container:
```bash
docker exec -it addon_XXXXXXXX_netbox /bin/bash

# Test SNMP manually
apt-get update && apt-get install -y snmp
snmpwalk -v2c -c public 192.168.1.1 system
```

### View Full Configuration

```bash
docker exec -it addon_XXXXXXXX_netbox cat /opt/netbox/netbox/netbox/configuration.py
```

### Restart NetBox

After making changes:
```bash
# From Home Assistant
# Settings → Add-ons → NetBox → Restart
```

## 7. What Gets Created

When a device is discovered, the plugin creates:

1. **Manufacturer** - Detected from device (Cisco, Juniper, etc.) or "Generic"
2. **Device Type** - From device model/description
3. **Device Role** - "Auto-Discovered"
4. **Site** - From SNMP location or "Default Site"
5. **Platform** - Detected OS (IOS, NX-OS, Junos, etc.)
6. **Device** - The actual device object
7. **Management Interface** - With the IP assigned
8. **Additional Interfaces** - Discovered via SNMP
9. **Tag** - "auto-discovered" (green)

## 8. Configuration Options

In Home Assistant addon options:

```yaml
device_autodiscovery_snmp_community: "public"  # SNMP community string
device_autodiscovery_enable_snmp: true         # Enable/disable SNMP
```

## 9. Quick Test Script

Create this test in NetBox:

1. Go to: Scripts → Add Script
2. Name: "Test Auto-Discovery"
3. Code:
```python
from ipam.models import IPAddress
from django.contrib.contenttypes.models import ContentType

# Create a test IP
ip = IPAddress.objects.create(
    address='192.168.99.99/32',
    status='active'
)
print(f"Created IP: {ip.address}")
print("Check logs for discovery activity!")
```

4. Run the script and watch the logs!

## Need Help?

- Check logs: `docker logs -f addon_XXXXXXXX_netbox`
- Report issues: https://github.com/TMA84/netbox-device-autodiscover/issues
- Plugin repo: https://github.com/TMA84/netbox-device-autodiscover
