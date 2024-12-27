import os
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from .utils import YoutubeDownloaderManager
from drf_spectacular.utils import extend_schema
from rest_framework import status 
from django.conf import settings



@extend_schema(
    tags=['Youtube Download'], 
    request={
        'application/json': {
            'properties': {
                'video_url': {'type': 'string', 'example': 'https://www.youtube.com/watch?v=tXjKPJ5KJUY'},
            }
        }
    },
    responses={
        200: {
            'properties': {
                'message': {'type': 'string', 'example': 'Téléchargement réussi.'},
                'media_url': {'type': 'string', 'example': 'http://localhost:8000/media/videos/video_name.mp4'},
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
            manager = YoutubeDownloaderManager()
            file_name = manager.download_mp4_video_to_link(video_url)
            
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




