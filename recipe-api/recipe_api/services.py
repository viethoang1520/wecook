import os
import logging
from datetime import datetime
from .utils import extract_audio_from_video
from .whisper_utils import transcribe_audio
from .recipe_processor import process_recipe

logger = logging.getLogger(__name__)

class RecipeService:
    def __init__(self, recipe_instance):
        self.recipe = recipe_instance
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_transcription_to_file(self, transcription_text):
        """Save transcription to a text file"""
        transcription_dir = os.path.join('media', 'transcriptions')
        os.makedirs(transcription_dir, exist_ok=True)
        
        # Create filename using timestamp and recipe ID
        filename = f'transcription_{self.recipe.id}_{self.timestamp}.txt'
        file_path = os.path.join(transcription_dir, filename)
        
        # Save transcription to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(transcription_text)
        
        return file_path

    def process_video(self):
        try:
            logger.info(f"Starting video processing for recipe {self.recipe.id}")
            
            # Create audio directory
            audio_dir = os.path.join('media', 'audios')
            os.makedirs(audio_dir, exist_ok=True)

            # Extract audio
            audio_path = os.path.join(audio_dir, f'audio_{self.timestamp}.mp3')
            logger.info(f"Extracting audio to {audio_path}")
            if not extract_audio_from_video(self.recipe.video.path, audio_path):
                raise Exception("Failed to extract audio from video")

            # Transcribe audio
            logger.info("Transcribing audio")
            transcription_result = transcribe_audio(audio_path)
            
            # Handle different possible result formats
            if isinstance(transcription_result, dict):
                transcription_text = transcription_result.get('text', '')
            else:
                transcription_text = str(transcription_result)
            
            # Save transcription to file
            transcription_path = self.save_transcription_to_file(transcription_text)
            logger.info(f"Transcription saved to: {transcription_path}")
            
            # Store transcription in model (optional, since we're saving to file)
            self.recipe.transcription = transcription_text
            self.recipe.save()

            if not transcription_text:
                raise Exception("Transcription result is empty")

            # Process recipe
            logger.info("Processing recipe")
            recipe_json = process_recipe(transcription_text)
            self.recipe.recipe_json = recipe_json
            self.recipe.status = 'completed'
            self.recipe.save()

            logger.info("Video processing completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error in process_video: {str(e)}")
            self.recipe.status = 'failed'
            self.recipe.error_message = str(e)
            self.recipe.save()
            return False