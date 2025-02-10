from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'video', 'timestamp', 'recipe_json', 'status', 'error_message']
        read_only_fields = ['timestamp', 'recipe_json', 'status', 'error_message']
