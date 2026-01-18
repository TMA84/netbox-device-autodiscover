# Configuration Guide - NetBox Device Auto-Discovery

The plugin can be configured in two ways:
1. **NetBox Web UI** (Recommended) - Configure via Admin panel
2. **Configuration File** - Set defaults in `configuration.py`

## Web UI Configuration (Recommended)

### Accessing Configuration

1. **Log in to NetBox** as an admin user
2. **Go to Admin Panel**:
   - Click your username (top right)
   - Click "Admin"
3. **Find Auto-Discovery Configuration**:
   - Look for "NETBOX_DEVICE_AUTODISCOVERY" section
   - Click "Auto-Discovery Configurations"
   - Click on the configuration (or "Add" if none exists)

### Configuration Options

#### General Settings

**Enabled**
- ☑️ Enable or disable automatic device discovery
- Default: `True`
- Uncheck to temporarily disable without removing the plugin

#### SNMP Settings

**SNMP Enabled**
- ☑️ Enable SNMP-based discovery
- Default: `True`
- Uncheck to disable SNMP and use only DNS

**SNMP Community**
- Text field for SNMP community string
- Default: `public`
- Example: `my-snmp-community`

**SNMP Version**
- Dropdown: v1, v2c, v3
- Default: `v2c`
- Most devices use v2c

**SNMP Timeout**
- Number of seconds to wait for SNMP response
- Default: `5`
- Increase for slow networks

#### DNS Settings

**DNS Enabled**
- ☑️ Enable DNS fallback when SNMP fails
- Default: `True`
- Uses reverse DNS lookup to get hostname

#### Default Assignments

**Default Site** ⭐
- Dropdown to select a site
- Default: `None` (creates from SNMP location)
- **Important**: Select a site here to avoid "must create site first" errors
- All discovered devices will be assigned to this site

**Default Device Role** ⭐
- Dropdown to select a device role
- Default: `None` (creates "Auto-Discovered" role)
- Select an existing role like "Network Device" or "Server"

**Default Tenant**
- Dropdown to select a tenant
- Default: `None`
- Assign all discovered devices to a specific tenant

**Default Location**
- Dropdown to select a location
- Default: `None`
- Assign all discovered devices to a specific location within the site

#### Behavior Settings

**Create Site from Location**
- ☑️ Automatically create sites from SNMP sysLocation field
- Default: `True`
- Uncheck if you want to use only the default site

**Create Interfaces**
- ☑️ Automatically discover and create network interfaces
- Default: `True`
- Uncheck to create only the management interface

**Set Primary IP**
- ☑️ Automatically set the discovered IP as the device's primary IP
- Default: `True`
- Uncheck if you want to manually set primary IPs

#### Naming

**Device Name Template**
- Template for device names
- Default: `{sysName}`
- Available variables:
  - `{sysName}` - From SNMP sysName
  - `{ip}` - IP address with dots replaced by dashes
  - `{hostname}` - From DNS lookup
- Examples:
  - `{sysName}` → `router-01`
  - `device-{ip}` → `device-192-168-1-1`
  - `{sysName}-{ip}` → `router-01-192-168-1-1`

## Recommended Configuration

### For First-Time Setup

1. **Create a default site first**:
   - Go to Organization → Sites → Add
   - Name: "Auto-Discovered Devices"
   - Save

2. **Configure the plugin**:
   - Admin → Auto-Discovery Configuration
   - Set **Default Site**: "Auto-Discovered Devices"
   - Set **Default Device Role**: Create or select "Network Device"
   - Set **SNMP Community**: Your network's SNMP community
   - Save

3. **Test it**:
   - Create an IP address in NetBox
   - Watch the logs
   - Check if device is created

### For Production Use

```
General Settings:
✓ Enabled: Yes

SNMP Settings:
✓ SNMP Enabled: Yes
  SNMP Community: your-community-string
  SNMP Version: v2c
  SNMP Timeout: 5

DNS Settings:
✓ DNS Enabled: Yes

Default Assignments:
  Default Site: [Select your main site]
  Default Device Role: [Select "Network Device" or similar]
  Default Tenant: [Optional - select if using tenants]
  Default Location: [Optional - select if using locations]

Behavior:
✓ Create Site from Location: No (use default site)
✓ Create Interfaces: Yes
✓ Set Primary IP: Yes

Naming:
  Device Name Template: {sysName}
```

## Configuration File Method

If you prefer to configure via `configuration.py`:

```python
PLUGINS_CONFIG = {
    'netbox_device_autodiscovery': {
        'snmp_community': 'public',
        'snmp_version': 2,
        'snmp_timeout': 5,
        'enable_snmp': True,
        'enable_ssh': False,
    }
}
```

**Note**: Web UI configuration takes precedence over file configuration.

## Common Configurations

### Scenario 1: All Devices to One Site

```
Default Site: "Main Data Center"
Create Site from Location: No
```

All devices go to "Main Data Center" regardless of SNMP location.

### Scenario 2: Create Sites from SNMP Location

```
Default Site: None
Create Site from Location: Yes
```

Plugin creates sites based on SNMP sysLocation field.

### Scenario 3: Specific Tenant for All Devices

```
Default Tenant: "IT Department"
```

All discovered devices are assigned to "IT Department" tenant.

### Scenario 4: Custom Device Names

```
Device Name Template: {sysName}-autodiscovered
```

Devices named like: `router-01-autodiscovered`

### Scenario 5: DNS Only (No SNMP)

```
SNMP Enabled: No
DNS Enabled: Yes
```

Uses only DNS reverse lookup for device names.

## Troubleshooting Configuration

### "Must create site first" Error

**Solution**: Set a **Default Site** in the configuration:
1. Admin → Auto-Discovery Configuration
2. Set "Default Site" to an existing site
3. Save

### "Must create manufacturer first" Error

**Solution**: This should be automatic. Check logs for errors.
If persists, manually create a "Generic" manufacturer.

### Devices Not Being Created

**Check**:
1. Is "Enabled" checked?
2. Is "SNMP Enabled" or "DNS Enabled" checked?
3. Check logs: `docker logs -f addon_XXXXXXXX_netbox`

### Wrong Site Assignment

**Solution**: 
- Set "Default Site" to your preferred site
- Uncheck "Create Site from Location"

### Too Many Interfaces Created

**Solution**: Uncheck "Create Interfaces" to create only management interface.

## Viewing Current Configuration

### Via Web UI
Admin → Auto-Discovery Configuration → View

### Via Logs
Look for this line in logs:
```
📋 Using database configuration for discovery
```

### Via Django Shell
```bash
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py shell
```

```python
from netbox_device_autodiscovery.models import AutoDiscoveryConfig
config = AutoDiscoveryConfig.get_config()
print(f"Enabled: {config.enabled}")
print(f"Default Site: {config.default_site}")
print(f"SNMP Community: {config.snmp_community}")
```

## Best Practices

1. **Always set a Default Site** to avoid errors
2. **Test with one IP first** before bulk imports
3. **Use meaningful device name templates** for easy identification
4. **Set a Default Device Role** to categorize devices properly
5. **Monitor logs** during initial setup
6. **Disable temporarily** instead of uninstalling if you need to pause discovery

## Security Considerations

- **SNMP Community**: Use a read-only community string
- **SNMP Version**: Use v3 with authentication when possible
- **Access Control**: Limit who can modify the configuration
- **Tenant Isolation**: Use tenants to separate device ownership

## Next Steps

After configuration:
1. Read [HOW_TO_SEE_IT_WORKING.md](HOW_TO_SEE_IT_WORKING.md) to test
2. Read [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing
3. Create your first IP address and watch it work!
