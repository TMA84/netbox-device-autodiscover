# How to See the Plugin Working 👀

## Quick Answer

**Watch the NetBox logs while creating an IP address!**

```bash
# Open a terminal and run this:
docker logs -f addon_XXXXXXXX_netbox

# Then in NetBox web UI:
# 1. Go to IPAM → IP Addresses → Add
# 2. Enter an IP address (e.g., 192.168.1.1/24)
# 3. Click Create
# 4. Watch the terminal - you'll see the discovery happen in real-time!
```

## What You'll See

### In the Logs (Terminal):

```
🔍 NEW IP ADDRESS DETECTED: 192.168.1.1/24
🚀 Starting automatic device discovery for 192.168.1.1...
🔎 Attempting SNMP discovery for 192.168.1.1 with community 'public'...
✅ SNMP discovery successful for 192.168.1.1
   - System Name: router-01
   - Description: Cisco IOS Software, C2900 Software...
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

### In NetBox Web UI:

1. **Go to Devices → Devices**
   - You'll see the new device appear automatically!
   - It has a green "auto-discovered" tag

2. **Click on the device** to see:
   - Manufacturer (e.g., Cisco, Juniper)
   - Device Type (detected from SNMP)
   - Site (from SNMP location)
   - Platform (e.g., Cisco IOS)
   - All interfaces discovered
   - Your IP assigned to the management interface

3. **Go to the IP Address** you created:
   - It's now assigned to the device's management interface
   - Shows as the device's primary IP

## Step-by-Step Test

### 1. Open Two Windows

**Window 1 - Terminal:**
```bash
docker logs -f addon_XXXXXXXX_netbox
```

**Window 2 - Browser:**
Open NetBox web UI

### 2. Create an IP Address

In NetBox:
1. IPAM → IP Addresses → Add
2. Address: `192.168.1.1/24` (or any IP)
3. Status: Active
4. Click "Create"

### 3. Watch the Magic!

**In Terminal (Window 1):**
- You'll see the discovery process in real-time
- Each step is logged with emojis (🔍 🚀 ✅)
- Takes 5-10 seconds

**In Browser (Window 2):**
- Go to Devices → Devices
- Refresh the page
- New device appears!

## If You Don't See Anything

### Check 1: Is the plugin installed?

```bash
docker exec -it addon_XXXXXXXX_netbox /opt/netbox/.venv/bin/pip list | grep netbox-device
```

Should show: `netbox-device-autodiscovery    1.0.0`

### Check 2: Is the plugin loaded?

```bash
docker logs addon_XXXXXXXX_netbox | grep "Device Auto-Discovery"
```

Should show: `Info: Configuring Device Auto-Discovery Plugin..`

### Check 3: Any errors?

```bash
docker logs addon_XXXXXXXX_netbox | grep -i error | tail -20
```

## What If SNMP Doesn't Work?

**No problem!** The plugin falls back to DNS:

```
🔍 NEW IP ADDRESS DETECTED: 192.168.1.100/24
🚀 Starting automatic device discovery...
🔎 Attempting SNMP discovery...
⚠️  SNMP discovery failed: Timeout
🔎 Attempting DNS lookup for 192.168.1.100...
✅ DNS lookup successful: my-server.local
📝 Creating device in NetBox...
✅ SUCCESS! Created device: my-server.local
```

Even without SNMP, you get:
- Device created with hostname from DNS
- IP assigned to management interface
- Tagged as "auto-discovered"

## Real-World Example

Let's say you have a Cisco router at 192.168.1.1:

1. **You create the IP in NetBox**
2. **Plugin discovers via SNMP:**
   - Name: "ROUTER-MAIN"
   - Manufacturer: Cisco
   - Model: Cisco 2900 Series
   - Location: "Data Center Rack 42"
   - 8 interfaces

3. **NetBox now has:**
   - Device: ROUTER-MAIN
   - Manufacturer: Cisco
   - Device Type: Cisco 2900 Series
   - Site: Data Center Rack 42
   - Platform: Cisco IOS
   - 8 interfaces (GigabitEthernet0/0, etc.)
   - IP 192.168.1.1 assigned to Management interface
   - Green "auto-discovered" tag

**All created automatically in seconds!**

## Pro Tips

### Tip 1: Keep Logs Open
Always have `docker logs -f` running when testing - it's the best way to see what's happening.

### Tip 2: Test with Different Devices
- Router with SNMP → Full discovery
- Server without SNMP → DNS fallback
- Non-existent IP → Generates name from IP

### Tip 3: Check the Tag
All auto-discovered devices have a green "auto-discovered" tag. Filter by this tag to see all devices created by the plugin.

### Tip 4: Look at Device Comments
Each device has a comment showing:
- "Auto-discovered from IP X.X.X.X"
- Full SNMP description

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| No logs appear | Check plugin is installed: `pip list \| grep netbox-device` |
| "Module not found" error | Rebuild addon with updated Dockerfile |
| SNMP timeout | Check SNMP is enabled on device, community string is correct |
| Device not created | Check logs for errors, verify IP is not already assigned |
| Wrong manufacturer | Plugin detects from SNMP description, may need manual correction |

## Summary

**To see it working:**
1. Open terminal: `docker logs -f addon_XXXXXXXX_netbox`
2. Open NetBox web UI
3. Create an IP address
4. Watch the logs show the discovery process
5. Check Devices list for the new device

**That's it!** The plugin works automatically every time you create an IP address.

For detailed testing and troubleshooting, see [TESTING_GUIDE.md](TESTING_GUIDE.md)
