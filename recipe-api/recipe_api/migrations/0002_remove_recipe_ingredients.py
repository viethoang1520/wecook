# Generated by Django 5.1.4 on 2024-12-10 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("recipe_api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="ingredients",
        ),
    ]
