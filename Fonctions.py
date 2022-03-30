import re

#Convertir les elements scraper en liste
def Mettre_en_liste(element):
    Liste = []
    for a in element:
        Liste.append(a.text.replace('\n', ', '))
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
