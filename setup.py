from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='netbox-device-autodiscovery',
    version='1.0.0',
    description='NetBox plugin for automatic device discovery when IP addresses are created',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='NetBox Plugin',
    author_email='[email]',
    url='https://github.com/yourusername/netbox-device-autodiscovery',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pysnmp>=4.4.12',
        'netmiko>=3.4.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
