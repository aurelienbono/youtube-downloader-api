

import time
import logging
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from django.conf import settings

# ✅ Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

def youtube_downloader_full_manager(YOUTUBE_VIDEO_URL):
    CUSTOM_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    # ✅ Configuration du WebDriver
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={CUSTOM_HEADERS['User-Agent']}")
    chrome_options.add_argument("--headless")  # Mode sans interface graphique
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    logging.info("🚀 Initialisation du WebDriver Chrome...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    logging.info("✅ WebDriver Chrome initialisé avec succès.")

    try:
        download_urls = []
        
        logging.info(f"🌐 Accès au site de téléchargement avec URL : {YOUTUBE_VIDEO_URL}")
        driver.get("https://ssyoutube.online/")
        time.sleep(3)

        # ✅ Saisie de l'URL de la vidéo dans le champ d'entrée
        logging.info("📥 Saisie de l'URL de la vidéo dans le champ d'entrée...")
        input_box = driver.find_element(By.XPATH, '//*[@id="videoURL"]')
        input_box.send_keys(YOUTUBE_VIDEO_URL)
        input_box.send_keys(Keys.RETURN)

        time.sleep(10)  # Attente pour le chargement de la page

        # ✅ Extraction des liens de téléchargement
        logging.info("🔍 Extraction des liens de téléchargement...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find("table")

        if table:
            logging.info("✅ Tableau de téléchargement trouvé.")
            buttons = table.find_all("button", {"onclick": True})

            for button in buttons:
                onclick_text = button["onclick"]
                match = re.search(r"onVideoOptionSelected\(this, '([^']+)'", onclick_text)

                if match:
                    video_url = match.group(1)
                    download_urls.append(video_url)
                    logging.info(f"🎥 Lien de téléchargement récupéré : {video_url}")
                else:
                    logging.warning("⚠️ Lien non trouvé dans l'attribut onclick.")

        else:
            logging.warning("⚠️ Aucun tableau de téléchargement trouvé.")

        return download_urls

    except Exception as e:
        logging.error(f"❌ Erreur : {e}")
        return []

    finally:
        logging.info("🛑 Fermeture du WebDriver...")
        driver.quit()