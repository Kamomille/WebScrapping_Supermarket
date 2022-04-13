import re
import os
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

def AdressesAuchan(url):
    driver.get(url)

    time.sleep(1)
    driver.find_element(by="id", value="onetrust-reject-all-handler").click()
    
    Adresses = driver.find_elements(by="class name", value="place-pos__address")
    Liste_Adresses = Fonctions.Mettre_en_liste(Adresses)
    Liste_Adresses = Fonctions.Format_Postal_Commune(Liste_Adresses, 0)

    return Liste_Adresses


def RecupCodePostalCsv():
    path = 'casino_csv_final'
    name_list = []
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            regex = re.compile("casino__([0-9]{5})")
            resultat = regex.search(filename)
            resultat = resultat.group(1)
            if resultat is None:
                pass
            else:
                name_list.append(resultat)
    new_list_name = []
    for i in name_list:
        if i not in new_list_name:
            new_list_name.append(i)
    return new_list_name

def RecupCodePostalCasino():
    CodePostal = driver.find_elements(by="class name", value="store-line__address")
    Liste_CodePostal = Fonctions.Mettre_en_liste(CodePostal)

    return Liste_CodePostal

def AdressesCasino(url):
    driver.get(url)

    time.sleep(1)
    driver.find_element(by="id", value="onetrust-reject-all-handler").click()

    time.sleep(1)
    Fonctions.Openheader(driver)

    CodePostalCsv = RecupCodePostalCsv()
    CodePostalRecup = RecupCodePostalCasino()
    Adresse_Casino = []
    for CodePostal in CodePostalCsv:
        for Code in CodePostalRecup:
            regex = re.compile("[0-9]{5}")
            resultat = regex.search(Code)
            if resultat is None:
                pass
            else:
                resultat = resultat.group(0)

            if CodePostal == resultat:
                Adresse_Casino.append(Code)

    Adresse_CasinoTri = []
    for i in Adresse_Casino:
        if i not in Adresse_CasinoTri:
            Adresse_CasinoTri.append(i)

    return Adresse_CasinoTri


Liste_Adresse_Auchan = AdressesAuchan("https://www.auchan.fr/nos-magasins?types=DRIVE")

Adresses_Auchan = {'Adresse': Liste_Adresse_Auchan}
df_Adresse_Auchan = pd.DataFrame(Adresses_Auchan)
df_Adresse_Auchan.to_csv('Adresse1.csv', index=False)


Liste_Adresse_casino = AdressesCasino("https://www.casino.fr/prehome/courses-en-ligne/magasins")

Adresses_Casino = {'Adresse': Liste_Adresse_casino}
df_Adresse_casino = pd.DataFrame(Adresses_Casino)
df_Adresse_casino.to_csv('Adresse1.csv', mode='a', index=False, header=False)


geocoder = Nominatim(user_agent="myGeocoder")
file = open('Adresse1.csv', 'r')
csv = csv.reader(file, delimiter=';')
next(csv)
Lat = []
Long = []

for ad in csv:
    location = geocoder.geocode(str(ad), country_codes="FR")
    print(ad)

    if location is None:
        print("None1")
        ad = Fonctions.Format_Postal_Commune(ad, 1)
        #print(str(ad))
        location_v2 = geocoder.geocode(ad, country_codes="FR")

        if location_v2 is None:
            print("None2")
            ad = Fonctions.Format_Postal_Commune(ad, 2)
            #print(str(ad))
            location_v3 = geocoder.geocode(ad, country_codes="FR")
            if location_v3 is None:
                print("None3")

            else:
                print((location_v3.latitude, location_v3.longitude))
                Lat.append(location_v3.latitude)
                Long.append(location_v3.longitude)
        else:
            print((location_v2.latitude, location_v2.longitude))
            Lat.append(location_v2.latitude)
            Long.append(location_v2.longitude)
    else:
        print((location.latitude, location.longitude))
        Lat.append(location.latitude)
        Long.append(location.longitude)


LatLong = {'Lat': Lat, 'Long': Long}
df_LatLong = pd.DataFrame(LatLong)
df_LatLong.to_csv('LatLong.csv', index=False)

df_Adresse = pd.read_csv('Adresse1.csv')
Liste_Adresse = list(df_Adresse["Adresse"])

df_LatLong = pd.read_csv('LatLong.csv')
Lat = list(df_LatLong["Lat"])
Long = list(df_LatLong["Long"])

my_map = folium.Map(location=[48.8911554, 2.2329507], zoom_start=7)

for i in range(1, 178):
    folium.Marker([float(Lat[i]), float(Long[i])], popup=str(Liste_Adresse[i])).add_to(my_map)

for j in range(179, 241):
    folium.Marker([float(Lat[j]), float(Long[j])], popup=str(Liste_Adresse[j]), icon=folium.Icon(color="green")).add_to(my_map)

my_map.save("carte.html")


