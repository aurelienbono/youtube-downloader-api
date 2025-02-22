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
import random  # 📌 Pour sélectionner un proxy aléatoire

# ✅ Configuration des logs
logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  
)

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

logging.info("🚀 Initialisation du WebDriver Chrome...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
logging.info("✅ WebDriver Chrome initialisé avec succès.")

# 📌 Liste de proxys gratuits (tu peux la mettre à jour régulièrement)
PROXY_LIST = [
    "https://103.137.110.146:7777", 
    "https://50.169.222.243:80",
    "https://51.254.78.223:80", 
    "https://4.149.210.210:3128",  
    "https://143.42.66.91:80", 
    "https://192.73.244.36:80", 
    "https://47.56.110.204:8989", 
    "https://50.217.226.41:80", 
    "https://162.223.90.130:80", 
    "https://87.248.129.26:80", 
    "https://50.207.199.81:80", 
    "https://190.103.177.131:80",
    "https://103.133.26.11:8080"
]

def get_random_proxy():
    """ Retourne un proxy aléatoire de la liste """
    return random.choice(PROXY_LIST)

def youtube_downloader_full_manager(YOUTUBE_VIDEO_URL):
    try:
        download_urls = []
        downloaded_files = []
        ua = UserAgent().chrome  # 📌 Génération d'un User-Agent dynamique
        proxy = get_random_proxy()  # 📌 Sélection aléatoire d’un proxy
        proxies = {"http": proxy, "https": proxy}  # 📌 Ajout du proxy

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
                logging.info(f"⬇️ Téléchargement de la vidéo depuis {video_url} en utilisant le proxy {proxy} ...")
                headers = {"User-Agent": ua}  # 📌 Ajout de l'User-Agent

                try:
                    video_response = requests.get(video_url, headers=headers, proxies=proxies, stream=True)

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

                except requests.exceptions.RequestException as e:
                    logging.error(f"❌ Échec du téléchargement via proxy {proxy}, erreur : {e}")
                    continue  # 📌 Passe au prochain lien en cas d’échec

        return downloaded_files

    except Exception as e:
        logging.error(f"❌ Erreur : {e}")
        return []

    finally:
        logging.info("🛑 Fermeture du WebDriver...")
        driver.quit()
