# image_extractor.py
from PIL import Image
import exifread
from .base_extractor import BaseMetadataExtractor
from pathlib import Path

class ImageMetadataExtractor(BaseMetadataExtractor):
    def supported_mime_types(self):
        return ['image/jpeg', 'image/png', 'image/gif', 'image/heic', 'image/webp']
    
    def extract(self, file_path: Path) -> Dict:
        metadata = {}
        
        with Image.open(file_path) as img:
            metadata['dimensions'] = {
                'width': img.width,
                'height': img.height,
                'mode': img.mode,
                'format': img.format
            }
        
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                if tags:
                    metadata['exif'] = {
                        str(k): str(v) 
                        for k, v in tags.items()
                        if k not in ('JPEGThumbnail', 'TIFFThumbnail')
                    }
        except Exception as e:
            metadata['exif_error'] = str(e)
        
        return metadata