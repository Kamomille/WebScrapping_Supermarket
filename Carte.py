import csv
import time
import folium
import pandas as pd
from selenium import webdriver
from geopy.geocoders import Nominatim
import Fonctions


driver = webdriver.Firefox()
driver.get("https://www.auchan.fr/nos-magasins")

time.sleep(1)
driver.find_element_by_id("onetrust-reject-all-handler").click()

time.sleep(1)
Adresse = driver.find_elements_by_class_name("place-pos__address")
Liste_Adresse = Fonctions.Mettre_en_liste(Adresse)

driver.close()

Code_commune = Fonctions.code_Postal(Liste_Adresse)
print(len(Code_commune))

df_Code_Commune = pd.DataFrame(data=Code_commune, columns=["Code Postal et Commune"])
df_Code_Commune.to_csv('CodeCommune.csv', index=False)

"""
print(Liste_Commune)
print(len(Liste_Adresse))
print(len(Liste_Commune))

"""
geocoder = Nominatim(user_agent="myGeocoder")
file = open('CodeCommune.csv', 'r')
csv = csv.reader(file, delimiter=';')
Lat = []
Long = []

for ad in csv:
    C_P = str(ad)
    location = geocoder.geocode(C_P, country_codes = "FR")
    #print((location.latitude, location.longitude))

    if location is None:
        print("None")
    else:
        print((location.latitude, location.longitude))
        Lat.append(location.latitude)
        Long.append(location.longitude)

print(len(Lat))
print(len(Long))
df_commune = pd.read_csv("CodeCommune.csv")

my_map = folium.Map(location = [48.8911554, 2.2329507], zoom_start = 15)

for i in range(len(Lat)):
    folium.Marker([float(Lat[i]), float(Long[i])], popup=str(Code_commune[i])).add_to(my_map)

my_map.save("carte.html")






