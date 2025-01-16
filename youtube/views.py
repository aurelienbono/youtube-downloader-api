import os
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from .utils import * 
import re
from drf_spectacular.utils import extend_schema
from rest_framework import status 
from django.conf import settings




@extend_schema(
    tags=['Video Download'], 
    request={
        'application/json': {
            'properties': {
                'video_url': {'type': 'string', 'example': 'https://twitter.com/somevideo'},
            }
        }
    },
    responses={
        200: {
            'properties': {
                'message': {'type': 'string', 'example': 'Téléchargement réussi.'},
                'media_url': {'type': 'string', 'example': 'http://url_of_Server:8000/media/videos/video_name.mp4'},
            }
        },
        400: {'properties': {'error': {'type': 'string', 'example': 'Le paramètre "video_url" est requis.'}}}
    }
)
@api_view(['POST'])
def download_mp4_video_to_link(request): 
    video_url = request.data.get("video_url", None)
    
    if video_url:
        try:
            youtube_patterns = [
                r'https?://(?:www\.)?(youtube\.com|youtu\.be)/.+',
            ]
            
            twitter_patterns = [
            r'https?://(?:www\.)?(twitter\.com|x\.com)/.+/status/\d+',
            ]

            if any(re.match(pattern, video_url) for pattern in youtube_patterns):
                manager = YoutubeDownloaderManager()
                file_name = manager.download_mp4_video_to_link(video_url)
            
            elif "drive.google.com" in video_url and "/file/d/" in video_url:
                manager = GoogleDriverDownloaderManager()
                file_name = manager.download_google_drive_file(video_url)
            
            elif any(re.match(pattern, video_url) for pattern in twitter_patterns):
                manager = TwitterDownloaderManager()
                file_name = manager.download_video_to_link(video_url)
            
            else:
                manager = FacebookManagerDownloader()
                file_name = manager.download_video_to_link(video_url)
            
            media_url = f"{settings.MEDIA_URL}videos/{file_name}"
            media_url = request.build_absolute_uri(media_url)
            
            return Response(
                {"message": "Téléchargement réussi.", "media_url": media_url},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Erreur lors du téléchargement de la vidéo.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            {"error": "Le paramètre 'video_url' est requis."},
            status=status.HTTP_400_BAD_REQUEST
        )

