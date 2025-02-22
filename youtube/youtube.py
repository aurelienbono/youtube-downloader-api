import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import os
from uuid import uuid4
from django.conf import settings

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Laisser Selenium gérer l'installation de ChromeDriver
driver = webdriver.Chrome(options=chrome_options)


def youtube_downloader_full_manager(YOUTUBE_VIDEO_URL):
    try:
        download_urls = []
        downloaded_files = []

        driver.get("https://ssyoutube.online/")
        time.sleep(3) 

        input_box = driver.find_element(By.XPATH, '//*[@id="videoURL"]')
        input_box.send_keys(YOUTUBE_VIDEO_URL)
        input_box.send_keys(Keys.RETURN)

        time.sleep(10)  

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        table = soup.find("table")

        if table:
            mp4_rows = table.find_all("tr", class_="mp4")
            if mp4_rows:
                for row in mp4_rows:
                    button = row.find("button", onclick=True)
                    if button:
                        match = re.search(r"window\.location\.href='(.*?)'", button["onclick"])
                        if match:
                            download_urls.append(match.group(1))
                            print(f"🎥 Lien de téléchargement trouvé : {match.group(1)}")
                        else : 
                            print("⚠️ Lien non trouvé dans l'attribut onclick.")
                            
                    else : 
                        print("⚠️ Pas de bouton trouvé dans cette ligne.")
                        
            else : 
                print("⚠️ Aucune ligne <tr class='mp4'> trouvée.")

        else:
            print("⚠️ Aucun tableau de téléchargement trouvé.")
               
               
               
                         
        if download_urls:
            download_path = os.path.join(settings.MEDIA_ROOT, 'videos')
            os.makedirs(download_path, exist_ok=True)

            for index, video_url in enumerate(download_urls):
                video_response = requests.get(video_url, stream=True)

                if video_response.status_code == 200:
                    video_filename = f"video_{index + 1}_{uuid4()}.mp4"
                    
                    video_path = os.path.join(download_path, video_filename)

                    with open(video_path, "wb") as f:
                        for chunk in video_response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)

                    downloaded_files.append(os.path.join(settings.MEDIA_URL, 'videos', video_filename))
                    print(f"✅ Vidéo téléchargée avec succès")
                else : 
                    print(f"❌ Erreur lors du téléchargement, code HTTP : {video_response.status_code}")

        return downloaded_files

    except Exception as e:
        print(f"❌ Erreur : {e}")
        return []

    finally:
        driver.quit()
