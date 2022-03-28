import re
import csv
import time
import folium
import pandas as pd
from selenium import webdriver
from geopy.geocoders import Nominatim
import Fonctions

driver = webdriver.Firefox()
driver.get("https://www.auchan.fr/nos-magasins?types=DRIVE")

time.sleep(1)
driver.find_element_by_id("onetrust-reject-all-handler").click()

time.sleep(1)
Adresse = driver.find_elements_by_class_name("place-pos__address")
Liste_Adresse = Fonctions.Mettre_en_liste(Adresse)
Liste_Adresse = Fonctions.Format_Postal_Commune(Liste_Adresse, 0)
driver.close()

""" 
Code_commune = Fonctions.code_Postal(Liste_Adresse)
print(len(Code_commune))
"""

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


df_LatLong = pd.DataFrame(list(zip(Lat, Long)), columns=["Lat", "Long"])
df_LatLong.to_csv('LatLong.csv', index=True)
print(len(Lat))
print(len(Long))

my_map = folium.Map(location = [48.8911554, 2.2329507], zoom_start = 15)

for i in range(len(Lat)):
    folium.Marker([float(Lat[i]), float(Long[i])], popup=str(Liste_Adresse[i])).add_to(my_map)

my_map.save("carte.html")



