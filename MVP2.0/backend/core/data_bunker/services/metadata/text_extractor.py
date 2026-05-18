# text_extractor.py
from .base_extractor import BaseMetadataExtractor
from pathlib import Path
import chardet
from typing import Dict

class TextMetadataExtractor(BaseMetadataExtractor):
    def supported_mime_types(self):
        return ['text/plain', 'text/csv', 'application/json']
    
    def extract(self, file_path: Path) -> Dict:
        metadata = {}
        
        try:
            # 检测文本编码
            with open(file_path, 'rb') as f:
                raw_data = f.read(4096)
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
                
            with open(file_path, 'r', encoding=encoding) as f:
                lines = sum(1 for _ in f)
                metadata.update({
                    'line_count': lines,
                    'encoding': encoding
                })
        except Exception as e:
            metadata['text_error'] = str(e)
        
        return metadata