import re
import csv
import time
import folium
import pandas as pd
from selenium import webdriver
from geopy.geocoders import Nominatim
import Fonctions

driver = webdriver.Firefox()
"""
driver.get("https://www.auchan.fr/nos-magasins?types=DRIVE")

time.sleep(1)
driver.find_element(by="id", value="onetrust-reject-all-handler").click()

time.sleep(1)
Adresse_Auchan = driver.find_elements(by="class name", value="place-pos__address")
Liste_Adresse_Auchan = Fonctions.Mettre_en_liste(Adresse_Auchan)
Liste_Adresse_Auchan = Fonctions.Format_Postal_Commune(Liste_Adresse_Auchan, 0)
"""
time.sleep(1)
driver.get("https://www.casino.fr/prehome/courses-en-ligne/magasins")

time.sleep(1)
driver.find_element(by="id", value="onetrust-reject-all-handler").click()

time.sleep(1)
#driver.close()

button = driver.find_elements(by="xpath", value="//button[@class='accordion__header accordion__header--no-shadow']")
print(len(button))
for j in button:
     j.click()

""" 
Liste = driver.find_elements(by='xpath',
                             value="//span[@class='store-list__accordion-header store-list__accordion-header--white']")
Liste_Drive_Casino = Fonctions.Mettre_en_liste(Liste)

print(Liste_Drive_Casino)
print(len(Liste_Drive_Casino))

for dot in Liste_Drive_Casino:
  regex = re.compile(".")
  resultat = regex.search(dot)
  if resultat is None:
      pass
  else:
      resultat = resultat.group(0)
      Liste_Drive_Casino.remove(str(resultat))

print(Liste_Drive_Casino)
print(len(Liste_Drive_Casino))
"""

Adresse_Casino = driver.find_elements(by = "class name", value="store-line__address")
Adresse_Casino = Fonctions.Mettre_en_liste(Adresse_Casino)
print(Adresse_Casino)
print(len(Adresse_Casino))


"""

Liste_Adresse_Casino = []
Adresse_Casino = driver.find_elements(by="xpath", value="//div[@class='Column Column-3']")
for Adr in Adresse_Casino:
    elems = Adr.find_elements(by='css selector', value="a")
    for elem in elems:
        Liste_Adresse_Casino.append(elem.get_attribute("href"))

print(len(Liste_Adresse_Casino))


Code_commune = Fonctions.code_Postal(Liste_Adresse)
print(len(Code_commune))


df_Adresse_Auchan = pd.DataFrame(data=Liste_Adresse, columns=["Adresse_auchan"])
df_Adresse_Auchan.to_csv('Adresse.csv', index=False)

print(len(Liste_Adresse))


geocoder = Nominatim(user_agent="myGeocoder")
file = open('Adresse.csv', 'r')
csv = csv.reader(file, delimiter=';')
next(csv)
Lat = []
Long = []

for ad in csv:
    location = geocoder.geocode(str(ad), country_codes = "FR")
    #print((location.latitude, location.longitude))

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
        #print((location.latitude, location.longitude))
        Lat.append(location.latitude)
        Long.append(location.longitude)


df_LatLong = pd.DataFrame(list(zip(Liste_Adresse, Lat, Long)), columns=["Adresse", "Lat", "Long"])
df_LatLong.to_csv('Adresses_auchan.csv', index=False)
print(len(Lat))
print(len(Long))


my_map = folium.Map(location = [48.8911554, 2.2329507], zoom_start = 15)

for i in range(len(Lat)):
    folium.Marker([float(Lat[i]), float(Long[i])], popup=str(Liste_Adresse[i])).add_to(my_map)

my_map.save("carte.html")
"""


