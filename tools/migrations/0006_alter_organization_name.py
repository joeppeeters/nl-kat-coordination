# Generated by Django 3.2.5 on 2021-10-26 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tools", "0005_scanprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="name",
            field=models.CharField(max_length=126, unique=True),
        ),
    ]
