#!/bin/bash
# Script to build and publish the package to PyPI

set -e

echo "=== NetBox Device Auto-Discovery - PyPI Publishing Script ==="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade build tools
echo "Installing build tools..."
pip install --upgrade pip build twine

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Build the package
echo "Building package..."
python -m build

echo ""
echo "=== Build Complete! ==="
echo ""
echo "Package files created in dist/:"
ls -lh dist/

echo ""
echo "=== Next Steps ==="
echo ""
echo "1. First, test on TestPyPI (recommended):"
echo "   twine upload --repository testpypi dist/*"
echo ""
echo "2. Test installation from TestPyPI:"
echo "   pip install --index-url https://test.pypi.org/simple/ netbox-device-autodiscovery"
echo ""
echo "3. If everything works, upload to PyPI:"
echo "   twine upload dist/*"
echo ""
echo "You'll need:"
echo "  - PyPI account: https://pypi.org/account/register/"
echo "  - API token: https://pypi.org/manage/account/token/"
echo ""
echo "When prompted for username, enter: __token__"
echo "When prompted for password, enter your API token"
echo ""
