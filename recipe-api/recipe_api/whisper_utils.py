import torch
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

def format_timestamp(seconds):
    """Convert seconds to [X.XXs] format"""
    return f"[{seconds:.2f}s]"

def format_transcription_segment(start, end, text):
    """Format a single transcription segment"""
    return f"[{start:.2f}s -> {end:.2f}s]  {text}"

def transcribe_audio(audio_path):
    """Transcribe audio using Whisper model"""
    try:
        logger.info(f"Starting transcription for: {audio_path}")
        
        # Use smaller model for CPU
        model_id = "openai/whisper-small"
        
        # Create pipeline with simpler configuration
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            chunk_length_s=30,
            return_timestamps=True  # Make sure to get timestamps
        )

        logger.info("Transcribing audio...")
        result = pipe(
            audio_path,
            generate_kwargs={"language": "vi", "task": "transcribe"}
        )
        
        # Format the transcription with timestamps
        if isinstance(result, dict) and 'chunks' in result:
            # For newer versions that return chunks
            formatted_lines = [
                format_transcription_segment(chunk['timestamp'][0], chunk['timestamp'][1], chunk['text'])
                for chunk in result['chunks']
            ]
        else:
            # For versions that return timestamps differently
            chunks = result.get('chunks', [])
            formatted_lines = [
                format_transcription_segment(chunk.get('start', 0), chunk.get('end', 0), chunk.get('text', ''))
                for chunk in chunks
            ]
        
        formatted_transcription = '\n'.join(formatted_lines)
        
        logger.info("Transcription completed successfully")
        return {'text': formatted_transcription}

    except Exception as e:
        logger.error(f"Error in transcribe_audio: {str(e)}")
        raise Exception(f"Transcription failed: {str(e)}")