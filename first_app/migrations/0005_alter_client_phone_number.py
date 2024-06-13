# Generated by Django 5.0.3 on 2024-04-27 07:16

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("first_app", "0004_alter_vehicle_client"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region=None
            ),
        ),
    ]