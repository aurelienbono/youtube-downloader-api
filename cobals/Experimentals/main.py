# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # import logging
# # import time
# # import random

# # # Configuration du service ChromeDriver
# # service = Service('chromedriver.exe')

# # # Configuration des options pour le mode headless et désactiver les indicateurs d'automatisation
# # options = webdriver.ChromeOptions()
# # # options.add_argument('--headless')
# # options.add_argument('--disable-gpu')  # Option nécessaire sur certaines plateformes
# # options.add_argument("--disable-blink-features=AutomationControlled")
# # options.add_experimental_option("excludeSwitches", ["enable-automation"])
# # options.add_experimental_option("useAutomationExtension", False)

# # # Liste des User Agents
# # user_agents = [
# #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
# #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
# # ]

# # # Sélectionner un User Agent aléatoire
# # user_agent = random.choice(user_agents)
# # options.add_argument(f'user-agent={user_agent}')

# # # Initialisation du WebDriver avec les options headless
# # logging.info("🚀 Initialisation du WebDriver Chrome en mode headless...")
# # driver = webdriver.Chrome(service=service, options=options)
# # logging.info("✅ WebDriver Chrome initialisé avec succès en mode headless.")

# # # Modifier la propriété de navigator.webdriver
# # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


# # YOUTUBE_VIDEO_URL = "https://youtu.be/cFCGUjc33aU?list=PL8motc6AQftn-X1HkaGG9KjmKtWImCKJS"

# # try:
# #     logging.info(f"🌐 Accès au site de téléchargement avec URL : {YOUTUBE_VIDEO_URL}")
# #     driver.get('https://cobalt.tools/')

# #     input_box = WebDriverWait(driver, 10).until(
# #         EC.presence_of_element_located((By.XPATH, '//*[@id="link-area"]'))
# #     )

# #     logging.info("📥 Saisie de l'URL de la vidéo dans le champ d'entrée...")
# #     input_box.send_keys(YOUTUBE_VIDEO_URL)
# #     input_box.send_keys(Keys.RETURN)

# #     time.sleep(5)

# #     screenshot_path = 'screenshot.png'
# #     driver.save_screenshot(screenshot_path)
# #     logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")

# #     time.sleep(5)

# #     screenshot_path = 'screenshot1.png'
# #     driver.save_screenshot(screenshot_path)
# #     logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")
    
    
# #     modal_button = WebDriverWait(driver, 20).until(
# #         EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog-save-error"]/div[1]/div[3]/button'))
# #     )
# #     modal_button.click()
# #     logging.info("✅ Modal validée.")
    
    

# #     download_button = WebDriverWait(driver, 20).until(
# #         EC.element_to_be_clickable((By.XPATH, '//*[@id="download-button"]'))
# #     )

# #     screenshot_path = 'screenshot2.png'
# #     driver.save_screenshot(screenshot_path)
# #     logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")

# #     time.sleep(5)

# #     screenshot_path = 'screenshot3.png'
# #     driver.save_screenshot(screenshot_path)
# #     logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")

# #     download_button.click()
# #     logging.info("✅ Bouton de téléchargement cliqué.")



# #     time.sleep(100)

# # finally:
# #     # Fermer le navigateur
# #     driver.quit()




# import undetected_chromedriver as uc


# options = uc.ChromeOptions()
# # options.headless = True
# # options.add_argument( '--headless' )
# chrome = uc.Chrome( options = options )
# chrome.get('https://cobalt.tools/')

# chrome.save_screenshot( 'datadome_undetected_webddriver.png' )





import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import os

# Configuration des options pour undetected-chromedriver
options = uc.ChromeOptions()
# options.headless = True  # Décommenter si vous souhaitez exécuter en mode headless

# Configurer le répertoire de téléchargement dans le dossier courant
download_dir = "./"
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Initialisation du WebDriver avec undetected-chromedriver
logging.info("🚀 Initialisation du WebDriver Chrome avec undetected-chromedriver...")
chrome = uc.Chrome(options=options)
logging.info("✅ WebDriver Chrome initialisé avec succès avec undetected-chromedriver.")

YOUTUBE_VIDEO_URL = "https://youtu.be/cFCGUjc33aU?list=PL8motc6AQftn-X1HkaGG9KjmKtWImCKJS"

try:
    # Accéder au site de téléchargement
    logging.info(f"🌐 Accès au site de téléchargement avec URL : {YOUTUBE_VIDEO_URL}")
    chrome.get('https://cobalt.tools/')

    # Attendre que le champ d'entrée soit présent
    input_box = WebDriverWait(chrome, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="link-area"]'))
    )

    # Saisir l'URL de la vidéo dans le champ d'entrée
    logging.info("📥 Saisie de l'URL de la vidéo dans le champ d'entrée...")
    input_box.send_keys(YOUTUBE_VIDEO_URL)
    input_box.send_keys(Keys.RETURN)

    time.sleep(5)

    # Prendre des captures d'écran
    screenshot_path = 'screenshot.png'
    chrome.save_screenshot(screenshot_path)
    logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")

    time.sleep(5)

    screenshot_path = 'screenshot1.png'
    chrome.save_screenshot(screenshot_path)
    logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")

    # Attendre que la modal soit présente et cliquer sur le bouton pour la valider
    modal_button = WebDriverWait(chrome, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="dialog-save-error"]/div[1]/div[3]/button'))
    )
    modal_button.click()
    logging.info("✅ Modal validée.")

    screenshot_path = 'screenshot3.png'
    chrome.save_screenshot(screenshot_path)
    logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")

    time.sleep(5)

    # Attendre que le bouton de téléchargement soit cliquable
    download_button = WebDriverWait(chrome, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="download-button"]'))
    )

    screenshot_path = 'screenshot2.png'
    chrome.save_screenshot(screenshot_path)
    logging.info(f"Capture d'écran enregistrée sous {screenshot_path}")

    time.sleep(5)

    # Cliquer sur le bouton de téléchargement
    download_button.click()
    logging.info("✅ Bouton de téléchargement cliqué.")

    # Attendre que le fichier soit téléchargé
    time.sleep(60)  # Ajustez ce délai en fonction de la taille du fichier et de la vitesse de votre connexion

    # Vérifier la présence du fichier téléchargé
    downloaded_files = os.listdir(download_dir)
    if downloaded_files:
        logging.info(f"Fichiers téléchargés : {downloaded_files}")
    else:
        logging.info("Aucun fichier téléchargé.")

finally:
    # Fermer le navigateur
    chrome.quit()
