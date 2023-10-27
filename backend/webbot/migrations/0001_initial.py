# Generated by Django 4.2.5 on 2023-10-18 01:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=120)),
                ("brand", models.CharField(blank=True, max_length=120, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("reviewNumber", models.IntegerField(default=0)),
                ("category", models.TextField(blank=True, max_length=999, null=True)),
                ("SKU", models.CharField(blank=True, max_length=65, null=True)),
                ("UPC", models.CharField(blank=True, max_length=65, null=True)),
                ("EAN", models.CharField(blank=True, max_length=65, null=True)),
                ("MPN", models.CharField(blank=True, max_length=65, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                ("user", models.CharField(max_length=120)),
                ("date", models.DateField(blank=True, null=True)),
                ("platform", models.CharField(max_length=120)),
                ("title", models.CharField(max_length=120)),
                ("text", models.TextField()),
                (
                    "rating",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0.0),
                            django.core.validators.MaxValueValidator(5.0),
                        ]
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="webbot.product"
                    ),
                ),
            ],
        ),
    ]
