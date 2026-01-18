# Publishing to PyPI

To make this plugin installable via `pip install netbox-device-autodiscovery`, follow these steps:

## Prerequisites

1. **Create PyPI Account**
   - Go to https://pypi.org/account/register/
   - Verify your email

2. **Create API Token**
   - Go to https://pypi.org/manage/account/token/
   - Create a token with "Entire account" scope
   - Save the token securely

## Prepare for Publishing

1. **Install Build Tools**
   ```bash
   pip install build twine
   ```

2. **Update Package Metadata**
   
   Edit `setup.py` with your actual information:
   ```python
   setup(
       name='netbox-device-autodiscovery',
       version='1.0.0',
       author='Your Name',
       author_email='your.email@example.com',
       url='https://github.com/yourusername/netbox-device-autodiscovery',
       # ... rest of setup
   )
   ```

3. **Ensure All Files Are Ready**
   - `setup.py` - Package configuration
   - `README.md` - Documentation
   - `LICENSE` - License file (create if missing)
   - `MANIFEST.in` - Include additional files
   - `requirements.txt` - Dependencies

## Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/netbox-device-autodiscovery-1.0.0.tar.gz` (source distribution)
- `dist/netbox_device_autodiscovery-1.0.0-py3-none-any.whl` (wheel)

## Test on TestPyPI First (Recommended)

1. **Create TestPyPI Account**
   - Go to https://test.pypi.org/account/register/

2. **Upload to TestPyPI**
   ```bash
   twine upload --repository testpypi dist/*
   ```

3. **Test Installation**
   ```bash
   pip install --index-url https://test.pypi.org/simple/ netbox-device-autodiscovery
   ```

## Publish to PyPI

1. **Upload to PyPI**
   ```bash
   twine upload dist/*
   ```
   
   Enter your PyPI username and API token when prompted.

2. **Verify Upload**
   - Visit https://pypi.org/project/netbox-device-autodiscovery/
   - Check that all information is correct

## Install from PyPI

Now anyone can install your plugin:

```bash
pip install netbox-device-autodiscovery
```

## For Home Assistant NetBox Addon

Once published to PyPI, users can install it in the NetBox container:

```bash
# Access the container
docker exec -it addon_XXXXXXXX_netbox /bin/bash

# Install the plugin
pip install netbox-device-autodiscovery

# Exit and restart the addon
exit
```

## Updating the Package

When you make changes:

1. **Update Version Number** in `setup.py`
   ```python
   version='1.0.1',  # Increment version
   ```

2. **Rebuild and Upload**
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   twine upload dist/*
   ```

## Using GitHub Actions for Automated Publishing

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add your PyPI token to GitHub Secrets as `PYPI_API_TOKEN`.

## Alternative: Install Directly from GitHub

If you don't want to publish to PyPI, users can install directly from GitHub:

```bash
pip install git+https://github.com/yourusername/netbox-device-autodiscovery.git
```

Or a specific version:

```bash
pip install git+https://github.com/yourusername/netbox-device-autodiscovery.git@v1.0.0
```

## Checklist Before Publishing

- [ ] All code is tested and working
- [ ] README.md is complete and accurate
- [ ] LICENSE file exists
- [ ] Version number is correct in setup.py
- [ ] Author information is updated
- [ ] GitHub repository URL is correct
- [ ] Dependencies are listed correctly
- [ ] Tested on TestPyPI first
- [ ] Package builds without errors
- [ ] .gitignore excludes build artifacts

## Support and Maintenance

After publishing:
- Monitor GitHub issues
- Respond to user questions
- Release updates for bug fixes
- Keep dependencies up to date
- Update documentation as needed
