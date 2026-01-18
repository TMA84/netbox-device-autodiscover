# Installing NetBox Device Auto-Discovery in Home Assistant Addon

Since NetBox runs as a Home Assistant addon, you need to install the plugin inside the addon's container.

## Method 1: Using the Addon's Configuration (Recommended)

1. **Access Home Assistant**
   - Go to Settings → Add-ons → NetBox

2. **Access the NetBox Container**
   ```bash
   # From Home Assistant terminal or SSH
   docker exec -it addon_XXXXXXXX_netbox /bin/bash
   ```

3. **Install the Plugin**
   
   NetBox uses `uv` as the package manager:
   
   ```bash
   # Inside the container
   uv pip install git+https://github.com/TMA84/netbox-device-autodiscover.git
   
   # Or if published to PyPI:
   uv pip install netbox-device-autodiscovery
   ```

4. **Configure NetBox**
   
   Edit the configuration file (usually at `/config/configuration.py` or `/data/configuration.py`):
   ```python
   PLUGINS = [
       'netbox_device_autodiscovery',
   ]
   
   PLUGINS_CONFIG = {
       'netbox_device_autodiscovery': {
           'snmp_community': 'public',
           'enable_snmp': True,
       }
   }
   ```

5. **Restart the Addon**
   - Go back to Home Assistant
   - Restart the NetBox addon

## Method 2: Create a Custom Addon (Better for Persistence)

Since addon containers are ephemeral, create a custom NetBox addon that includes this plugin.

1. **Fork the NetBox Home Assistant Addon Repository**

2. **Modify the Dockerfile** to include the plugin:
   ```dockerfile
   # Add to the existing Dockerfile
   COPY netbox-device-autodiscovery /tmp/netbox-device-autodiscovery
   RUN pip install /tmp/netbox-device-autodiscovery
   ```

3. **Add Configuration Template**
   
   Modify `rootfs/etc/netbox/configuration.py` to include:
   ```python
   PLUGINS = [
       'netbox_device_autodiscovery',
   ]
   
   PLUGINS_CONFIG = {
       'netbox_device_autodiscovery': {
           'snmp_community': '{{ .snmp_community }}',
           'enable_snmp': {{ .enable_snmp }},
       }
   }
   ```

4. **Update config.yaml** to add options:
   ```yaml
   options:
     snmp_community: "public"
     enable_snmp: true
   ```

5. **Build and Install Your Custom Addon**

## Method 3: Volume Mount (Easiest for Development)

1. **Prepare Plugin Directory**
   ```bash
   # On your Home Assistant host
   mkdir -p /config/netbox-plugins/netbox_device_autodiscovery
   
   # Copy plugin files
   cp -r netbox_device_autodiscovery/* /config/netbox-plugins/netbox_device_autodiscovery/
   ```

2. **Access NetBox Container**
   ```bash
   docker exec -it addon_XXXXXXXX_netbox /bin/bash
   ```

3. **Install from Mounted Volume**
   ```bash
   # Inside container - use uv
   uv pip install -e /config/netbox-plugins/netbox_device_autodiscovery
   ```

4. **Configure and Restart** (same as Method 1)

## Method 4: Install from GitHub (Easiest!)

Install directly from the GitHub repository:

```bash
# Inside the NetBox container
# First activate the NetBox virtual environment
source /opt/netbox/venv/bin/activate

# Then install from GitHub
pip install git+https://github.com/TMA84/netbox-device-autodiscover.git
```

## Method 5: Publish to PyPI (Best Long-term Solution)

To make it installable via `pip install netbox-device-autodiscovery`:

1. **Create PyPI Account** at https://pypi.org

2. **Install Build Tools**
   ```bash
   pip install build twine
   ```

3. **Build the Package**
   ```bash
   python -m build
   ```

4. **Upload to PyPI**
   ```bash
   twine upload dist/*
   ```

5. **Then Install in NetBox Container**
   ```bash
   # Inside the NetBox container
   uv pip install netbox-device-autodiscovery
   ```

## Persistence Considerations

Home Assistant addons may reset on updates. To maintain persistence:

- Use Method 2 (custom addon) for permanent installation
- Or create a startup script that reinstalls the plugin
- Or request the NetBox addon maintainer to include your plugin

## Troubleshooting

**Find NetBox Container Name:**
```bash
docker ps | grep netbox
```

**Check if Plugin is Installed:**
```bash
docker exec -it addon_XXXXXXXX_netbox uv pip list | grep netbox-device
```

**View Logs:**
```bash
docker logs -f addon_XXXXXXXX_netbox
```

**Access NetBox Shell:**
```bash
docker exec -it addon_XXXXXXXX_netbox python /opt/netbox/netbox/manage.py shell
```

## Recommended Approach for Home Assistant

For Home Assistant specifically, I recommend **Method 2** (custom addon) because:
- Survives addon updates
- Proper integration with HA configuration
- Can be shared with the community
- Maintains proper addon structure

Would you like me to create the files needed for a custom Home Assistant addon that includes this plugin?
