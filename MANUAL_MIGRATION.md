# Manual Migration Guide

If you installed the plugin and can't find the configuration interface, you need to run database migrations.

## Quick Fix

Run this command to create the database tables:

```bash
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py migrate netbox_device_autodiscovery
```

Replace `XXXXXXXX` with your actual addon ID (e.g., `878443c7`).

## Step-by-Step

### 1. Find Your Container ID

```bash
docker ps | grep netbox
```

Look for something like `addon_878443c7-netbox`

### 2. Run Migrations

```bash
# Replace addon_XXXXXXXX_netbox with your container name
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py migrate netbox_device_autodiscovery
```

You should see:
```
Running migrations:
  Applying netbox_device_autodiscovery.0001_initial... OK
```

### 3. Restart NetBox

In Home Assistant:
- Settings → Add-ons → NetBox
- Click "Restart"

### 4. Verify

After restart:

1. Log in to NetBox
2. Click your username → **Admin**
3. Look for **"NETBOX_DEVICE_AUTODISCOVERY"** section
4. You should see **"Auto-Discovery Configurations"**

## If Migrations Fail

### Error: "No such table"

This is normal on first run. The migration will create the table.

### Error: "Plugin not found" or "No installed app"

Check if plugin is installed:
```bash
docker exec -it addon_XXXXXXXX_netbox uv pip list | grep netbox-device
```

Should show: `netbox-device-autodiscovery    1.0.0`

If not installed, reinstall:
```bash
docker exec -it addon_XXXXXXXX_netbox uv pip install git+https://github.com/TMA84/netbox-device-autodiscover.git
```

### Error: "Module has no migrations"

The migrations folder might be missing. Check:
```bash
docker exec -it addon_XXXXXXXX_netbox ls -la /opt/netbox/.venv/lib/python*/site-packages/netbox_device_autodiscovery/migrations/
```

Should show `0001_initial.py` and `__init__.py`

### Error: "Permission denied"

Run as root or with sudo:
```bash
docker exec -it -u root addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py migrate netbox_device_autodiscovery
```

## Alternative: Rebuild Addon

If migrations don't work, rebuild the addon with the latest version:

1. **Update your addon repository** (if using custom fork)
2. **Rebuild the addon** in Home Assistant
3. **Restart NetBox**

The new version automatically runs migrations on startup.

## Verify Configuration Interface

After successful migration:

1. **Log in to NetBox** as admin
2. **Go to Admin panel**: Click username → Admin
3. **Look for**: "NETBOX_DEVICE_AUTODISCOVERY" section
4. **Click**: "Auto-Discovery Configurations"
5. **You should see**: Configuration form with all options

If you see the form, migrations were successful! ✅

## Create Initial Configuration

1. Click **"Add Auto-Discovery Configuration"** (if none exists)
2. Set at minimum:
   - **Default Site**: Select an existing site
   - **SNMP Community**: Your SNMP community string
3. Click **"Save"**

## Test It

1. Create an IP address in NetBox
2. Watch logs: `docker logs -f addon_XXXXXXXX_netbox`
3. Check if device is created

## Troubleshooting

### "Can't find configuration after migration"

Clear browser cache and refresh:
- Chrome/Edge: Ctrl+Shift+R (Cmd+Shift+R on Mac)
- Firefox: Ctrl+F5 (Cmd+Shift+R on Mac)

### "Configuration exists but can't edit"

Check permissions:
```bash
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py shell
```

```python
from netbox_device_autodiscovery.models import AutoDiscoveryConfig
config = AutoDiscoveryConfig.get_config()
print(f"Config exists: {config.id}")
print(f"Enabled: {config.enabled}")
```

### "Multiple configuration objects"

There should only be one. Delete extras:
```bash
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py shell
```

```python
from netbox_device_autodiscovery.models import AutoDiscoveryConfig
# Keep only the first one
configs = AutoDiscoveryConfig.objects.all()
for config in configs[1:]:
    config.delete()
```

## Future Installations

For new installations, migrations run automatically on addon startup. You only need to run manual migrations if:
- You installed the plugin before migrations were added
- You're upgrading from an older version
- The automatic migration failed

## Need Help?

- Check logs: `docker logs addon_XXXXXXXX_netbox`
- Report issues: https://github.com/TMA84/netbox-device-autodiscover/issues
- Include error messages and NetBox version
