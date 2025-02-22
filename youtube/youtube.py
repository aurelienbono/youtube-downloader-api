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
from fake_useragent import UserAgent

# ✅ Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def youtube_downloader_full_manager(YOUTUBE_VIDEO_URL):
        
    # ✅ Headers personnalisés
    CUSTOM_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
        "Connection": "keep-alive",
        "Host": "ssyoutube.online",
        "Sec-Ch-Ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    # ✅ Configuration du WebDriver
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={CUSTOM_HEADERS['User-Agent']}")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    logging.info("🚀 Initialisation du WebDriver Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    logging.info("✅ WebDriver Chrome initialisé avec succès.")

    
    
    
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
                downloaded_files.append(video_url)
       
        return downloaded_files
    
    except Exception as e:
        logging.error(f"❌ Erreur : {e}")
        return []
    
    finally:
        logging.info("🛑 Fermeture du WebDriver...")
        driver.quit()
