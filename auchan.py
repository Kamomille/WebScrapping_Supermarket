# -*- coding: utf-8 -*-
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

#driver = webdriver.Firefox()
#driver = webdriver.Chrome('C:\Program Files\chromedriver_win32\chromedriver.exe')

# -- Création du driver --
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
driver = webdriver.Firefox(firefox_profile=firefox_profile)
driver.get("https://www.auchan.fr/")
time.sleep(3)

# -- Click sur refuser --
driver.find_element_by_id("onetrust-reject-all-handler").click()
time.sleep(2)


# -- Création du CSV --
csvFile = open("auchan_produits.csv", "w", newline='', encoding="utf-8")
csvWriter = csv.writer(csvFile, delimiter=';', quotechar='"')

# -- Création du nom des colonnes --
csvWriter.writerow(['categorie', 'type', 'nom', 'poids', 'prix_par_kg', 'prix', 'promo'])

def xpath(num):
    return '/html/body/div[2]/aside/div[1]/main/nav/div[2]/div/div[11]/div/div[2]/div/div[' + str(num) + ']/div/a[1]'

list_epicerie_sucree = [['Cafe',xpath(1)],
                        ['Petit dej, boissons chaudes',xpath(2)],
                        ['Biscuits, gateaux',xpath(3)],
                        ['Chocolat, confiseries',xpath(3)],
                        ['Dessert, sucre, farine',xpath(4)]]


# ========================= Epicerie sucrée =============================================================

for i in range (len(list_epicerie_sucree)):

    # -- Ouvre le menu de navigation --
    driver.find_element_by_id("navigation").click()
    time.sleep(1)

    # -- Selectionne "Epicerie sucrée" --
    driver.find_element_by_xpath('//*[@id="navigation_layer_desc"]/nav/div[2]/div/div[11]/a').click()
    time.sleep(1)

    # -- Selectionne "Biscuits, gateaux" --
    driver.find_element_by_xpath(list_epicerie_sucree[i][1]).click()
    time.sleep(1)

    # ========================= Prix selon la localisation =============================================================

    if (i == 0):
        # -- Click sur "afficher le prix" --
        driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[4]/article[1]/div[2]/footer/button').click()
        time.sleep(2)
        # -- Cherche ville de paris + selectionne Paris 1er --
        element = driver.find_element_by_xpath('/html/body/div[11]/div[1]/main/div[1]/div[1]/div/div[1]/input')
        element.send_keys("Paris")
        time.sleep(2)
        element.send_keys(Keys.DOWN + Keys.ENTER)
        time.sleep(3)
        # -- Choisit la localisation numéro 1 --
        driver.find_element_by_xpath("/html/body/div[11]/div[1]/main/div[1]/div[2]/div[2]/section/div/div[2]/div/div/div[2]/form/button").click()
        time.sleep(10)

    # ========================= Scroll pour charger tous les éléments ======================================================

    # -- Scroll down --
    """
    SCROLL_PAUSE_TIME = 15
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight-1000")
    while True:
        # Scroll down jusqu'en bas
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
        # Attend (chargement page)
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculer la nouvelle hauteur de défilement et comparer avec la dernière hauteur de défilement
        new_height = driver.execute_script("return document.body.scrollHeight-1000")
        if new_height == last_height: break
        last_height = new_height
    """
    y = 1000
    for timer in range(0, 50):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 1000
        time.sleep(2)

    # ========================= Rempli le CSV =======================================================================

    # -- Selectionne les élements --
    searchresults_text = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[4]").find_elements_by_tag_name("article")

    for element in searchresults_text:
       txt = element.text.split("\n")
       if (len(txt) > 4):
          if (txt[0] == 'Nouveauté'): del txt[0]
          if (txt[0].isdigit() == True) : del txt[0]
          txt.remove("Avec ma livraison")
          print(txt)
          compt = -1
          promo = "non"
          for el in txt:
             if (el[-1] == 'g' and el[-2].isdigit() == True): poids = el
             if (el[-6:] == '€ / kg'): prix_par_kilo = el[:-6]
             if (el == 'Voir l\'offre'): promo = txt[compt]
             compt += 1

          # Ecriture dans le fichier CSV
          csvWriter.writerow(("Epicerie sucree",list_epicerie_sucree[i][0], txt[0], poids, prix_par_kilo, txt[-1].replace('€', ''), promo))

