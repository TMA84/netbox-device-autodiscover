# Generated migration for AutoDiscoveryConfig model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dcim', '0001_initial'),
        ('tenancy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoDiscoveryConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('enabled', models.BooleanField(default=True, help_text='Enable or disable automatic device discovery')),
                ('snmp_enabled', models.BooleanField(default=True, help_text='Enable SNMP-based discovery')),
                ('snmp_community', models.CharField(default='public', help_text='SNMP community string for device discovery', max_length=100)),
                ('snmp_version', models.IntegerField(choices=[(1, 'v1'), (2, 'v2c'), (3, 'v3')], default=2, help_text='SNMP version to use')),
                ('snmp_timeout', models.IntegerField(default=5, help_text='SNMP timeout in seconds')),
                ('dns_enabled', models.BooleanField(default=True, help_text='Enable DNS fallback when SNMP fails')),
                ('create_site_from_location', models.BooleanField(default=True, help_text='Automatically create sites from SNMP location field')),
                ('create_interfaces', models.BooleanField(default=True, help_text='Automatically discover and create interfaces')),
                ('set_primary_ip', models.BooleanField(default=True, help_text='Automatically set the discovered IP as primary IP')),
                ('device_name_template', models.CharField(default='{sysName}', help_text='Template for device names. Available variables: {sysName}, {ip}, {hostname}', max_length=200)),
                ('default_site', models.ForeignKey(blank=True, help_text='Default site for discovered devices (if not detected from SNMP location)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dcim.site')),
                ('default_device_role', models.ForeignKey(blank=True, help_text='Default device role for discovered devices', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dcim.devicerole')),
                ('default_tenant', models.ForeignKey(blank=True, help_text='Default tenant for discovered devices', null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenancy.tenant')),
                ('default_location', models.ForeignKey(blank=True, help_text='Default location for discovered devices', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dcim.location')),
            ],
            options={
                'verbose_name': 'Auto-Discovery Configuration',
                'verbose_name_plural': 'Auto-Discovery Configuration',
            },
        ),
    ]
