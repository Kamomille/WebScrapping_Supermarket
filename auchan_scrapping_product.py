# -*- coding: utf-8 -*-
import csv
import pandas as pd
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

df_adresse = pd.read_csv("Adresse.csv")

def xpath(num, num_grandes_categorie):
    return '/html/body/div[2]/aside/div[1]/main/nav/div[2]/div/div['+str(num_grandes_categorie)+']/div/div[2]/div/div['+str(num)+']/div/a[1]'

list_epicerie_sucree = ['Cafe','Petit dej, boissons chaudes','Biscuits, gateaux','Chocolat, confiseries','Dessert, sucre, farine']
list_fruit_legume = ['Bio','Fruit','Légumes','Prêt à consommer']

list_grandes_categorie = [['Fruits, légumes', list_fruit_legume],
                          ['Epicerie sucrée', list_epicerie_sucree]]

indicateur_a_t_on_deja_cliquer_sur_prix = False

for index_row in df_adresse.index:
    localisation = str(df_adresse["Adresse_auchan"][index_row]) #a[6:]
    type_pickup = "Drive"

    # -- Création du CSV --
    csvFile = open("auchan_csv/auchan_produits_"+localisation+".csv", "w", newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile, delimiter=';', quotechar='"')

    # -- Création du nom des colonnes --
    csvWriter.writerow(['categorie', 'type', 'nom', 'poids', 'prix_par_kg', 'prix', 'promo'])

    # ========================= catégorie =============================================================

    for j in range (len(list_grandes_categorie)):
        for i in range (len(list_grandes_categorie[j][1])):

            # -- Ouvre le menu de navigation --
            driver.find_element_by_id("navigation").click()
            time.sleep(2)

            # -- Selectionne la grande catégorie --
            for num in range (1, 12):
                nom = driver.find_element_by_xpath('/html/body/div[2]/aside/div[1]/main/nav/div[2]/div/div['+str(num)+']/a/span[2]').text
                if(nom == list_grandes_categorie[j][0]):
                    driver.find_element_by_xpath('/html/body/div[2]/aside/div[1]/main/nav/div[2]/div/div['+str(num)+']/a/span[2]').click()
                    time.sleep(1)
                    break
            time.sleep(2)
            # -- Selectionne une sous catégorie --
            driver.find_element_by_xpath(xpath(i+1, num)).click()
            time.sleep(2)

            # ========================= Prix selon la localisation =============================================================

            if (i == 0 and j == 0):
                if (indicateur_a_t_on_deja_cliquer_sur_prix == False):
                    # -- Click sur "afficher le prix" --
                    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[4]/article[1]/div[2]/footer/button').click()
                    indicateur_a_t_on_deja_cliquer_sur_prix = True
                else:
                    driver.find_element_by_xpath('/html/body/div[2]/header/div[1]/div[1]/div/button').click()
                time.sleep(2)
                # -- Cherche ville de paris + selectionne Paris 1er --
                element = driver.find_element_by_xpath('/html/body/div[11]/div[1]/main/div[1]/div[1]/div/div[1]/input')
                element.send_keys(localisation)
                time.sleep(2)
                element.send_keys(Keys.DOWN + Keys.ENTER)
                time.sleep(3)
                # -- Choisit la localisation parmi les choix de la liste --
                searchresults_text = driver.find_element_by_xpath("/html/body/div[11]/div[1]/main/div[1]/div[2]/div[2]/section/div").find_elements_by_class_name("place-pos__main-infos")
                list_type = []
                for element in searchresults_text:
                    element = element.text.split("\n")
                    list_type.append(element)
                    print(element)
                for k in range (len(list_type)):
                    if(list_type[k][0] == type_pickup): # and list_type[k][1] == localisation
                        print("OK")
                        driver.find_element_by_xpath("/html/body/div[11]/div[1]/main/div[1]/div[2]/div[2]/section/div/div["+ str(2+k) +"]/div/div/div[2]/form/button").click()
                        break
                    else : print("nope")
                time.sleep(5)

            # ========================= Scroll pour charger tous les éléments ======================================================

            # -- Scroll down --
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
               poids=""
               if (len(txt) > 4):
                  print(txt)
                  if (txt[0] == 'Nouveauté' or txt[0] == 'C\'est de saison !'): del txt[0]
                  if (txt[0][0] == '>' or txt[0] == 'Prix promo'): del txt[0]
                  if (txt[0][0:4] == 'Prix'): del txt[0]
                  if (txt[0].isdigit() == True) : del txt[0]
                  if ("Avec ma livraison" in txt) : txt.remove("Avec ma livraison")

                  compt = -1
                  promo = "non"
                  prix_par_kilo =""
                  for el in txt:
                     if (el[-1] == 'g' and el[-2].isdigit() == True and len(el) < 8): poids = el[:-1]
                     if (el[-6:] == '€ / kg' or el[-7:] == '€ / pce'): prix_par_kilo = el #[:-6]
                     if (el == 'Voir l\'offre'): promo = txt[compt]
                     compt += 1

                  l = list_grandes_categorie[j][1]
                  # Ecriture dans le fichier CSV
                  csvWriter.writerow((list_grandes_categorie[j][0],l[i], txt[0], poids, prix_par_kilo, txt[-1].replace('€', ''), promo))


# ========================= BROUILLON ==================================================================================

"""
lst1 = ["Hirson","Supermarché Massieux","St-Quentin","Viry Noureuil"]
lst2 = ["Drive","Click & Collect","Drive","Drive"]
df_localisation = pd.DataFrame(list(zip(lst1,lst2)), columns = ['nom_ville','type'])

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