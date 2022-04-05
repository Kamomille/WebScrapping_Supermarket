import re
import csv
import time
import folium
import pandas as pd
from selenium import webdriver
from geopy.geocoders import Nominatim
import Fonctions
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui

driver = webdriver.Firefox()
""" 
def RecupNomAuchan():
    Nom = driver.find_elements(by="class name", value="place-pos__name")
    Liste_Nom = Fonctions.Mettre_en_liste(Nom)
    return Liste_Nom

def AdressesAuchan(url):
    driver.get(url)

    time.sleep(1)
    driver.find_element(by="id", value="onetrust-reject-all-handler").click()
    
    Adresses = driver.find_elements(by="class name", value="place-pos__address")
    Liste_Adresses = Fonctions.Mettre_en_liste(Adresses)
    Liste_Adresses = Fonctions.Format_Postal_Commune(Liste_Adresses, 0)

    Liste_Nom = RecupNomAuchan()
    return Liste_Adresses, Liste_Nom

"""
def Openheader():
    button = driver.find_elements("xpath", "//button[@class='accordion__header accordion__header--no-shadow']")
    for j in button:
        j.click()

def OpenLinkInTab(link):
    link.send_keys(Keys.CONTROL + Keys.RETURN)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    New_window = driver.window_handles[1]
    driver.switch_to.window(New_window)
    time.sleep(3)

def CloseTab():
    driver.close()
    main_window = driver.window_handles[0]
    driver.switch_to.window(main_window)

def RecupNomCasino():
    Nom = driver.find_elements(by="class name", value="store-header__name")
    Liste_Nom = Fonctions.Mettre_en_liste(Nom)
    Liste_Nom
    for a in Liste_Nom:
        regex = re.compile("Supermarché ((.*)$)")
        resultat = regex.search(a)
        resultat = resultat.group(1)
        if resultat is None:
            pass
        else:
            Code_Postal.append(resultat)

    return Liste_Nom

def AdressesCasino(url):
    driver.get(url)

    time.sleep(1)
    driver.find_element(by="id", value="onetrust-reject-all-handler").click()

    time.sleep(1)
    Openheader()

    LineAction = driver.find_elements(by="xpath", value="//div[@class='store-line__actions']")
    liens_adresses = [i.find_element(by='css selector', value="a") for i in LineAction]

    Liste_Adresses=[]
    for lien in liens_adresses[2:]:
        OpenLinkInTab(lien)

        Adresse = driver.find_element(by="xpath", value="//div[@class='store-body__location-detail']")
        Liste_Adresses.append(Adresse.text)

        CloseTab()

    return Liste_Adresses
"""

Liste_Adresse_Auchan, Liste_Nom_Auchan = AdressesAuchan("https://www.auchan.fr/nos-magasins?types=DRIVE")

Adresses_Auchan = {'Drive': 'Auchan', 'Nom': Liste_Nom_Auchan, 'Adresse': Liste_Adresse_Auchan}
df_Adresse_Auchan = pd.DataFrame(Adresses_Auchan)
df_Adresse_Auchan.to_csv('Adresse.csv', index=False)

"""
Liste_Adresse_casino = AdressesCasino("https://www.casino.fr/prehome/courses-en-ligne/magasins")

Adresses_Casino = {'Nom' : 'Casino', 'Adresse' : Liste_Adresse_casino}
df_Adresse_casino = pd.DataFrame(Adresses_Casino)
df_Adresse_casino.to_csv('Adresse.csv', mode='a', index=False, header=False)
""" 

geocoder = Nominatim(user_agent="myGeocoder")
file = open('Adresse.csv', 'r')
csv = csv.reader(file, delimiter=';')
next(csv)
Lat = []
Long = []


def Test_Adresse_entiere(Adresse, Lat, Long):
    location = geocoder.geocode(str(Adresse), country_codes="FR")
    if location is None:
        print(None)
        return None
    else:
        Lat.append(location.latitude)
        Long.append(location.longitude)
        return Lat, Long

def Test_code_postal(Adresse, Lat, Long):
    location = geocoder.geocode(str(Adresse), country_codes="FR")
    if location is None:
        print(None)
        return None
    else:
        Fonctions.Format_Postal_Commune(Adresse, )
        Lat.append(location.latitude)
        Long.append(location.longitude)
        return Lat, Long


for ad in csv:
    location0 = geocoder.geocode(str(ad), country_codes = "FR")
    #print((location.latitude, location.longitude))

    if location0 is None:
        # print("None1")
        ad = Fonctions.Format_Postal_Commune(ad, 0)
        # print(str(ad))
        location = geocoder.geocode(ad, country_codes="FR")

        if location is None:
            #print("None1")
            ad = Fonctions.Format_Postal_Commune(ad, 1)
            #print(str(ad))
            location_v2 = geocoder.geocode(ad, country_codes="FR")

            if location_v2 is None:
                #print("None2")
                ad = Fonctions.Format_Postal_Commune(ad, 2)
                #print(str(ad))
                location_v3 = geocoder.geocode(ad, country_codes="FR")
                if location_v3 is None:
                    print("None3")

                else:
                    #print((location_v3.latitude, location_v3.longitude))
                    Lat.append(location_v3.latitude)
                    Long.append(location_v3.longitude)
            else:
                #print((location_v2.latitude, location_v2.longitude))
                Lat.append(location_v2.latitude)
                Long.append(location_v2.longitude)
        else:
            Lat.append(location.latitude)
            Long.append(location.longitude)
    else:
        Lat.append(location0.latitude)
        Long.append(location0.longitude)

df_Adresses = pd.DataFrame("Adresse.csv")
Liste_Adresse = df_Adresses.values.tolist()
df_Info_Adresse = pd.DataFrame(list(zip(Liste_Adresse, Lat, Long)), columns=["Adresses", "Lat", "Long"])
df_Info_Adresse.to_csv('InfosAdresses.csv', index=False)
print(len(Lat))
print(len(Long))


my_map = folium.Map(location = [48.8911554, 2.2329507], zoom_start = 15)

for i in range(len(Lat)):
    folium.Marker([float(Lat[i]), float(Long[i])], popup=str(Liste_Adresse[i])).add_to(my_map)

my_map.save("carte.html")

"""

