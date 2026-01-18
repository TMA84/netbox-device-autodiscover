# Quick Start Guide 🚀

## What You Have

✅ A complete NetBox plugin for automatic device discovery
✅ Package built and ready to publish to PyPI
✅ All files validated and passing checks

## To Publish to PyPI (3 Simple Steps)

### 1. Create PyPI Account
- Go to: https://pypi.org/account/register/
- Verify your email

### 2. Get API Token
- Go to: https://pypi.org/manage/account/token/
- Create token with "Entire account" scope
- Copy the token (starts with `pypi-`)

### 3. Upload
```bash
source .venv/bin/activate
twine upload dist/*
```
- Username: `__token__`
- Password: (paste your token)

**Done!** Your package will be live at: https://pypi.org/project/netbox-device-autodiscovery/

## To Install in Home Assistant

Install it right now from GitHub:

```bash
# One-line install (replace XXXXXXXX with your addon ID)
docker exec -it addon_XXXXXXXX_netbox /opt/netbox/.venv/bin/pip install git+https://github.com/TMA84/netbox-device-autodiscover.git

# Or once published to PyPI:
docker exec -it addon_XXXXXXXX_netbox /opt/netbox/.venv/bin/pip install netbox-device-autodiscovery
```

**After installation, run migrations:**

```bash
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py migrate netbox_device_autodiscovery
```

Then restart the NetBox addon from Home Assistant.

Then add to NetBox configuration:
```python
PLUGINS = ['netbox_device_autodiscovery']
PLUGINS_CONFIG = {
    'netbox_device_autodiscovery': {
        'snmp_community': 'public',
        'enable_snmp': True,
    }
}
```

Restart the NetBox addon and you're done!

## How It Works

1. Create an IP address in NetBox
2. Plugin automatically discovers the device via SNMP
3. Creates device with all information:
   - Manufacturer
   - Device Type
   - Site
   - Platform
   - Interfaces
   - Assigns the IP to management interface

## Files in This Project

- `netbox_device_autodiscovery/` - Plugin source code
- `dist/` - Built packages ready for PyPI
- `setup.py` - Package configuration
- `README.md` - Full documentation
- `PUBLISH_INSTRUCTIONS.md` - Detailed publishing guide
- `INSTALL_HOME_ASSISTANT.md` - HA-specific installation guide

## Need Help?

See `PUBLISH_INSTRUCTIONS.md` for detailed steps and troubleshooting.
