# Generated by Django 5.2.4 on 2025-07-16 03:42

import django.db.models.deletion
from django.db import migrations, models


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
                ("title", models.CharField(max_length=200)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("top", "Top"),
                            ("bottom", "Bottom"),
                            ("dress", "Dress"),
                            ("outerwear", "Outerwear"),
                            ("shoes", "Shoes"),
                            ("accessories", "Accessories"),
                        ],
                        max_length=20,
                    ),
                ),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("image", models.ImageField(upload_to="products/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="SizeChart",
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
                (
                    "label",
                    models.CharField(
                        choices=[
                            ("XS", "Extra Small"),
                            ("S", "Small"),
                            ("M", "Medium"),
                            ("L", "Large"),
                            ("XL", "Extra Large"),
                            ("XXL", "Double Extra Large"),
                        ],
                        max_length=3,
                        unique=True,
                    ),
                ),
                ("chest_min", models.FloatField(help_text="Minimum chest size in cm")),
                ("chest_max", models.FloatField(help_text="Maximum chest size in cm")),
                ("waist_min", models.FloatField(help_text="Minimum waist size in cm")),
                ("waist_max", models.FloatField(help_text="Maximum waist size in cm")),
                (
                    "recommended_height",
                    models.FloatField(help_text="Recommended height in cm"),
                ),
            ],
            options={
                "ordering": ["chest_min"],
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                ("image", models.ImageField(upload_to="products/gallery/")),
                ("alt_text", models.CharField(blank=True, max_length=100)),
                ("is_primary", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="available_sizes",
            field=models.ManyToManyField(blank=True, to="products.sizechart"),
        ),
    ]
