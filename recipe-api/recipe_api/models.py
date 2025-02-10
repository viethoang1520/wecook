from django.db import models

class Recipe(models.Model):
    video = models.FileField(upload_to='videos/')
    timestamp = models.DateTimeField(auto_now_add=True)
    transcription = models.TextField(blank=True, editable=False)
    recipe_json = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"Recipe {self.id} - {self.timestamp}"
