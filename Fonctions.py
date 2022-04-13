import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#Convertir les elements scraper en liste
def Mettre_en_liste(element):
    Liste = [a.text.lower().replace('\n', ', ') for a in element]
    return Liste


#Rechercher les code postales et communes et les mettre dans une liste
""" 
a permet de recuperer une partie du pattern
a = 0 -> Tout le pattern
a = 1 -> Seulement de code postal
a = 2 -> Seulement la commune
"""


def Format_Postal_Commune(Donnees, a):
    if a == 0:
        Code_Postal = []
        for Postal in Donnees:
            regex = re.compile("([0-9]{5}) ((.*)$)")
            resultat = regex.search(Postal)
            resultat = resultat.group(a).replace("Cedex", "")
            if resultat is None:
                pass
            else:
                Code_Postal.append(resultat)
        len(Code_Postal)
        return Code_Postal
    else:
        regex = re.compile("([0-9]{5}) ((.*)$)")
        resultat = regex.search(str(Donnees))
        if resultat is None:
            pass
        else:
            resultat = resultat.group(a)
            return resultat

def append(Location, Lat, Long):
    print((Location.latitude, Location.longitude))
    Lat.append(Location.latitude)
    Long.append(Location.longitude)
    return Lat, Long

def Openheader(driver):
    button = driver.find_elements("xpath", "//button[@class='accordion__header accordion__header--no-shadow']")
    for j in button:
        j.click()

def OpenLinkInTab(driver, link):
    link.send_keys(Keys.CONTROL + Keys.RETURN)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    New_window = driver.window_handles[1]
    driver.switch_to.window(New_window)
    time.sleep(2)

def CloseTab(driver):
    driver.close()
    main_window = driver.window_handles[0]
    driver.switch_to.window(main_window)