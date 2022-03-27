import re

#Convertir les elements scraper en liste
def Mettre_en_liste(element):
    Liste = []
    for a in range(len(element)):
        Liste.append(element[a].text.replace('\n', ', '))
    return Liste

#Rechercher les code postales et communes et les mettre dans une liste
def code_Postal(Liste_Postal):
    Code_Postal = []
    for Postal in Liste_Postal:
        regex = re.compile(", [0-9]{5}(.*)$")
        resultat = regex.search(Postal)
        resultat = resultat.group(0).replace("Cedex", "")
        resultat = resultat.replace(", ", "")
        if resultat is None:
            print (None)
        else:
            Code_Postal.append(resultat)
    len(Code_Postal)
    return Code_Postal

