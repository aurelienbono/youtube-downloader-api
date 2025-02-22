import time
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import os
from uuid import uuid4
from django.conf import settings

# ✅ Configuration des logs
logging.basicConfig(
    level=logging.INFO,  # Niveau INFO pour voir les messages importants
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Redirige les logs vers stdout pour Docker
)

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Utilisation de webdriver-manager pour gérer automatiquement ChromeDriver
logging.info("🚀 Initialisation du WebDriver Chrome...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
logging.info("✅ WebDriver Chrome initialisé avec succès.")

def youtube_downloader_full_manager(YOUTUBE_VIDEO_URL):
    try:
        download_urls = []
        downloaded_files = []

        logging.info(f"🌐 Accès au site de téléchargement avec URL : {YOUTUBE_VIDEO_URL}")
        driver.get("https://ssyoutube.online/")
        time.sleep(3)

        logging.info("📥 Saisie de l'URL de la vidéo dans le champ d'entrée...")
        input_box = driver.find_element(By.XPATH, '//*[@id="videoURL"]')
        input_box.send_keys(YOUTUBE_VIDEO_URL)
        input_box.send_keys(Keys.RETURN)

        time.sleep(10)

        logging.info("🔍 Extraction des liens de téléchargement...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table")

        if table:
            logging.info("✅ Tableau de téléchargement trouvé.")
            mp4_rows = table.find_all("tr", class_="mp4")
            if mp4_rows:
                for row in mp4_rows:
                    button = row.find("button", onclick=True)
                    if button:
                        match = re.search(r"window\.location\.href='(.*?)'", button["onclick"])
                        if match:
                            download_urls.append(match.group(1))
                            logging.info(f"🎥 Lien de téléchargement récupéré : {match.group(1)}")
                        else:
                            logging.warning("⚠️ Lien non trouvé dans l'attribut onclick.")
                    else:
                        logging.warning("⚠️ Pas de bouton trouvé dans cette ligne.")
            else:
                logging.warning("⚠️ Aucune ligne <tr class='mp4'> trouvée.")
        else:
            logging.warning("⚠️ Aucun tableau de téléchargement trouvé.")

        if download_urls:
            download_path = os.path.join(settings.MEDIA_ROOT, 'videos')
            os.makedirs(download_path, exist_ok=True)
            logging.info(f"📂 Dossier de téléchargement : {download_path}")

            for index, video_url in enumerate(download_urls):
                logging.info(f"⬇️ Téléchargement de la vidéo depuis {video_url}...")
                video_response = requests.get(video_url, stream=True)

                if video_response.status_code == 200:
                    video_filename = f"video_{index + 1}_{uuid4()}.mp4"
                    video_path = os.path.join(download_path, video_filename)

                    with open(video_path, "wb") as f:
                        for chunk in video_response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)

                    downloaded_file_url = os.path.join(settings.MEDIA_URL, 'videos', video_filename)
                    downloaded_files.append(downloaded_file_url)
                    logging.info(f"✅ Vidéo téléchargée avec succès : {downloaded_file_url}")
                else:
                    logging.error(f"❌ Erreur HTTP {video_response.status_code} lors du téléchargement.")

        return downloaded_files

    except Exception as e:
        logging.error(f"❌ Erreur : {e}")
        return []

    finally:
        logging.info("🛑 Fermeture du WebDriver...")
        driver.quit()
