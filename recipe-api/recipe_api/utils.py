import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def extract_audio_from_video(video_path, output_audio_path):
    """Extract audio from video using FFmpeg"""
    try:
        if not os.path.exists(os.path.dirname(output_audio_path)):
            os.makedirs(os.path.dirname(output_audio_path))
            
        command = [
            "ffmpeg",
            "-i", video_path,
            "-q:a", "0",
            "-map", "a",
            output_audio_path
        ]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error extracting audio: {e}")
        return False