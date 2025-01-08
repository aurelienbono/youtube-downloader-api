import yt_dlp
import os
from django.conf import settings
from uuid import uuid4
import gdown
import subprocess


class YoutubeDownloaderManager:
    def __init__(self):
        self.download_path = os.path.join(settings.MEDIA_ROOT, 'videos')
        os.makedirs(self.download_path, exist_ok=True)

    def download_video(self, video_url):
        custom_name = f"{str(uuid4()).replace('-', '')}_ma_video.mp4"
        custom_path = os.path.join(self.download_path, custom_name)

        ydl_opts = {
            'format': 'mp4',
            'outtmpl': custom_path, 
            'restrictfilenames': True,   
            'noplaylist': True, 
            'cookiefile': os.path.join(os.path.dirname(__file__), '../cookies.txt'),           
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(video_url, download=True)
            return custom_name  
        except Exception as e:
            raise Exception(f"Erreur lors du téléchargement : {str(e)}")

    def download_mp4_video_to_link(self, video_url):
        file_name = self.download_video(video_url.strip())
        return file_name




class GoogleDriverDownloaderManager:
    def __init__(self):
        pass
    
    def download_google_drive_file(self, file_url):
        download_path = os.path.join(settings.MEDIA_ROOT, 'videos')
        os.makedirs(download_path, exist_ok=True)
        
        custom_name = f"{str(uuid4()).replace('-', '')}_ma_video.mp4"
        custom_path = os.path.join(download_path, custom_name)
        
        if "drive.google.com" in file_url and "/file/d/" in file_url:
            file_id = file_url.split("/file/d/")[1].split("/")[0]
            file_url = f"https://drive.google.com/uc?id={file_id}"
        
        gdown.download(file_url, custom_path, quiet=False)
        
        if custom_path.endswith('.part'):
            final_path = custom_path.replace('.part', '.mp4')
            os.rename(custom_path, final_path)
            custom_name = final_path.split(os.path.sep)[-1]  

        return custom_name
    
    

class FacebookManagerDownloader:
    def __init__(self):
        self.download_path = os.path.join(settings.MEDIA_ROOT, 'videos')
        os.makedirs(self.download_path, exist_ok=True)

    def download_facebook_video(self, video_url):
        custom_name = f"{str(uuid4()).replace('-', '')}_ma_video.mp4"
        custom_path = os.path.join(self.download_path, custom_name)

        command = [
            "yt-dlp",
            "--format", "bestvideo",
            "--output", custom_path,
            "--restrict-filenames",
            "--noplaylist",
            "--cookiefile", os.path.join(os.path.dirname(__file__), '../cookies_fb.txt'),
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            video_url.strip()
        ]
        try:
            subprocess.run(command, check=True)
            return custom_name  
        except subprocess.CalledProcessError as e:
            raise Exception(f"Erreur lors du téléchargement de la vidéo Facebook : {str(e)}")

    def download_video_to_link(self, video_url):
        return self.download_facebook_video(video_url)

