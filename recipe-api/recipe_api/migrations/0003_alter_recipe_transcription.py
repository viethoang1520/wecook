# Generated by Django 5.1.4 on 2024-12-11 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipe_api", "0002_remove_recipe_ingredients"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="transcription",
            field=models.TextField(blank=True, editable=False),
        ),
    ]
