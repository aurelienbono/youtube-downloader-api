import yt_dlp
import os
from django.conf import settings
from uuid import uuid4

class YoutubeDownloaderManager:
    def __init__(self):
        self.download_path = os.path.join(settings.MEDIA_ROOT, 'videos')
        os.makedirs(self.download_path, exist_ok=True)

    def download_video(self, video_url):
        # Génération d'un nom unique pour le fichier (UUID)
        custom_name = f"{str(uuid4()).replace('-', '')}_ma_video.mp4"
        custom_path = os.path.join(self.download_path, custom_name)

        # Options pour yt-dlp
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': custom_path,  # Force le chemin et le nom personnalisé
            'restrictfilenames': True,  # Évite les caractères spéciaux ou les espaces
            'noplaylist': True,  # Télécharge uniquement une vidéo, pas une playlist
        }

        try:
            # Téléchargement avec yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(video_url, download=True)
            return custom_name  # Retourne uniquement le nom du fichier
        except Exception as e:
            raise Exception(f"Erreur lors du téléchargement : {str(e)}")

    def download_mp4_video_to_link(self, video_url):
        # Téléchargement de la vidéo
        file_name = self.download_video(video_url.strip())
        return file_name
