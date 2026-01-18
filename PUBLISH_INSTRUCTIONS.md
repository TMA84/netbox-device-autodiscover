# Ready to Publish to PyPI! 🚀

Your package has been built successfully! Here's what to do next:

## Files Created

✅ `dist/netbox_device_autodiscovery-1.0.0.tar.gz` - Source distribution
✅ `dist/netbox_device_autodiscovery-1.0.0-py3-none-any.whl` - Wheel distribution

## Step 1: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Fill in your details and verify your email
3. Enable 2FA (recommended)

## Step 2: Create API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Token name: `netbox-device-autodiscovery`
4. Scope: "Entire account" (for first upload)
5. Click "Add token"
6. **IMPORTANT**: Copy the token immediately (starts with `pypi-`)
7. Save it securely - you won't see it again!

## Step 3: Test on TestPyPI First (Recommended)

Before publishing to the real PyPI, test on TestPyPI:

1. Create TestPyPI account: https://test.pypi.org/account/register/
2. Create API token: https://test.pypi.org/manage/account/token/

3. Upload to TestPyPI:
```bash
source .venv/bin/activate
twine upload --repository testpypi dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your TestPyPI token)

4. Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ netbox-device-autodiscovery
```

## Step 4: Publish to PyPI

Once you've tested on TestPyPI and everything works:

```bash
source .venv/bin/activate
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: (paste your PyPI token)

## Step 5: Verify

1. Visit: https://pypi.org/project/netbox-device-autodiscovery/
2. Check that all information looks correct
3. Test installation:
```bash
pip install netbox-device-autodiscovery
```

## For Home Assistant NetBox Addon

Once published, users can install it:

```bash
# Access the NetBox container
docker exec -it addon_XXXXXXXX_netbox /bin/bash

# Install the plugin
pip install netbox-device-autodiscovery

# Exit
exit
```

Then add to NetBox configuration and restart the addon.

## Troubleshooting

**Error: "The user 'USERNAME' isn't allowed to upload"**
- Make sure you're using `__token__` as username (with two underscores)
- Check that your token is correct

**Error: "File already exists"**
- The version already exists on PyPI
- Update version in `setup.py` and rebuild

**Error: "Invalid distribution"**
- Check that all required files are present
- Verify setup.py is correct

## Updating the Package

When you make changes:

1. Update version in `setup.py`:
```python
version='1.0.1',  # Increment version
```

2. Rebuild:
```bash
source .venv/bin/activate
rm -rf dist/ build/
python -m build
```

3. Upload:
```bash
twine upload dist/*
```

## Quick Commands Reference

```bash
# Activate virtual environment
source .venv/bin/activate

# Build package
python -m build

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Check package
twine check dist/*
```

## Need Help?

- PyPI Help: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/
- Twine Docs: https://twine.readthedocs.io/

---

**You're all set!** The package is built and ready to upload. Just follow the steps above to publish it to PyPI.
