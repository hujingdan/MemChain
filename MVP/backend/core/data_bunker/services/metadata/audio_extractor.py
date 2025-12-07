# audio_extractor.py
import mutagen
from .base_extractor import BaseMetadataExtractor
from pathlib import Path

class AudioMetadataExtractor(BaseMetadataExtractor):
    def supported_mime_types(self):
        return ['audio/mpeg', 'audio/wav', 'audio/flac', 'audio/aac']
    
    def extract(self, file_path: Path) -> Dict:
        metadata = {}
        
        try:
            audio = mutagen.File(file_path, easy=True)
            if audio:
                metadata.update({
                    'duration': audio.info.length,
                    'bitrate': audio.info.bitrate,
                    'sample_rate': audio.info.sample_rate,
                    'channels': audio.info.channels
                })
                
                if audio.tags:
                    metadata['tags'] = {
                        key: value[0] if len(value) == 1 else value
                        for key, value in audio.tags.items() if key != 'LYRICS'
                    }
        except Exception as e:
            metadata['mutagen_error'] = str(e)
        
        return metadata