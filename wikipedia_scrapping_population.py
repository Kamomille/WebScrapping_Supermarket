import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

# -- Création du driver --
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
driver = webdriver.Firefox(firefox_profile=firefox_profile)


df_adresse = pd.read_csv("pop.csv", sep=',')
df = df_adresse.copy()

indicateur_a_t_on_deja_cliquer_sur_accepter = False
list_population = []

for index_row in df.index:
    localisation = str(df["Adresse_auchan"][index_row])

    driver.get("https://www.google.com/")
    time.sleep(3)

    # -- Click sur accepter les conditions --
    if(indicateur_a_t_on_deja_cliquer_sur_accepter == False):
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/button[2]/div").click()
        indicateur_a_t_on_deja_cliquer_sur_accepter = True
        time.sleep(4)

    # -- Barre de recherche --
    element = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
    element.send_keys('wikipedia population ' + localisation)
    element.send_keys(Keys.ENTER)
    time.sleep(4)

    # -- Sélectionne le 1er lien --
    driver.find_element_by_tag_name('h3').click()
    time.sleep(4)

    # --  --
    searchresults_text = driver.find_elements_by_tag_name("tr")

    nb_habitant = 'Pas trouvé'
    for element in searchresults_text:
       txt = element.text.split("\n")
       if (txt[0] == 'Population'  and txt[1][:10]== 'municipale'):
           a = txt[1][11:]
           b = a.split('hab')
           nb_habitant = int(b[0].replace(' ', ''))
           print(localisation, ' : ', nb_habitant)
           list_population.append(nb_habitant)
           break
    if (nb_habitant == 'Pas trouvé'):
        list_population.append('nan')
        print('PAS TROUVER pour ',localisation)
    time.sleep(4)

df = df.assign(population=list_population)
# Enregister
df.to_csv("adresse_auchan_population.csv", sep=',',index=False)

