# video_extractor.py
import ffmpeg
from .base_extractor import BaseMetadataExtractor
from pathlib import Path

class VideoMetadataExtractor(BaseMetadataExtractor):
    def supported_mime_types(self):
        return ['video/mp4', 'video/quicktime', 'video/x-msvideo']
    
    def extract(self, file_path: Path) -> Dict:
        metadata = {}
        
        try:
            probe = ffmpeg.probe(str(file_path))
            video_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'video'), None)
            audio_stream = next(
                (s for s in probe['streams'] if s['codec_type'] == 'audio'), None)
            
            metadata.update({
                'duration': float(probe['format']['duration']),
                'video_codec': video_stream.get('codec_name') if video_stream else None,
                'resolution': f"{video_stream.get('width')}x{video_stream.get('height')}" if video_stream else None,
                'audio_codec': audio_stream.get('codec_name') if audio_stream else None,
                'frame_rate': float(video_stream['avg_frame_rate'].split('/')[0]) 
                            if video_stream and 'avg_frame_rate' in video_stream else None
            })
        except Exception as e:
            metadata['ffprobe_error'] = str(e)
        
        return metadata