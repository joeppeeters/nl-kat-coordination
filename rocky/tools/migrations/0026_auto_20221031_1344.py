# Generated by Django 3.2.16 on 2022-10-31 13:44

from django.db import migrations
from django.contrib.auth.management import create_permissions


# https://stackoverflow.com/a/40092780/1336275
def migrate_permissions(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None


def add_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    can_set_clearance_level = Permission.objects.get(codename="can_set_clearance_level")
    try:
        redteam = Group.objects.get(name="redteam")
        redteam.permissions.add(can_set_clearance_level)
    except Group.DoesNotExist:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("tools", "0025_auto_20221027_1233"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(migrate_permissions),
        migrations.RunPython(add_group_permissions),
    ]
