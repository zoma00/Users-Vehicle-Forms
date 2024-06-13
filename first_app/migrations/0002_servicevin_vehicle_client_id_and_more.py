# Generated by Django 5.0.3 on 2024-04-24 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("first_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceVIN",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("vin", models.CharField(max_length=17, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name="vehicle",
            name="service_vin",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="first_app.servicevin"
            ),
        ),
    ]