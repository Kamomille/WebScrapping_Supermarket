import csv
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

#
#                                       SITE + COOKIES ACCEPTE

driver = webdriver.Firefox()
site = "https://www.casino.fr/prehome/courses-en-ligne/magasins"
driver.get(site)
driver.set_window_position(-1000, 0)
driver.maximize_window()
button = WebDriverWait(driver, 100).until(
    EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))).click()
time.sleep(2)
y = 50

def scrolltoBottom():
    time.sleep(3)
    y = 1000
    for timer in range(0, 40):
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y += 1000
        time.sleep(1)

def getNbrProduits():
    try:
        popup_close = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[1]/a'))).click()
    except WebDriverException:
        print("0")
        time.sleep(2)
    burger_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/div[2]/div[3]"))).click()
    nom_cat=driver.find_element_by_xpath("/html/body/div[2]/header/nav/div/ul/li[4]/div/div/div").text
    print(nom_cat)
    rayon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/div"))).click()
    l_sous_rayons = driver.find_elements_by_xpath("//div[@class='list-container']")
    for sr in range(1, len(l_sous_rayons)):
        print(sr)
        sous_rayon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/ul/div/li[" + str(sr) + "]/div"))).click()
        click_rayon = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 "/html/body/div[2]/header/nav/div/ul/li[4]/ul/div/li[" + str(sr) + "]/ul/div/div/div[3]/a"))).click()
        scrolltoBottom()
        list_nbr_produits = driver.find_elements_by_class_name("product-item__bottom")
        return len(list_nbr_produits)

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


def GetLinkShop():
    LineAction = driver.find_elements(by="xpath", value="//div[@class='store-line__actions']")
    liens_adresses = [i.find_element(by='css selector', value="a") for i in LineAction]
    for lien in liens_adresses[3:]:
        OpenLinkInTab(lien)
        mag=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[1]/div/ol/li[4]/span").text
        print(mag)
        # mag = driver.find_element_by_class_name(
        # "base-breadcrumb__item base-breadcrumb__item--text base-breadcrumb__item--last base-breadcrumb__item--white").text
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div[2]/div/div/a").click()
        n=getNbrProduits()
        #mag=getNomMag()
        getCSV(n, mag)
        CloseTab()

def getNomMag():
     time.sleep(3)
     y = 0
     driver.execute_script("window.scrollTo(0, " + str(y) + ")")
     driver.find_element_by_xpath("/html/body/div[2]/header/div[1]/div/a[1]/span").click()
     nom_mag = driver.find_element_by_xpath("/html/body/div[2]/header/div[1]/div/div/ul/li[2]/a/span[2]/em").text
     print(nom_mag)
     return nom_mag



def getCSV(nbr_produits, nom_mag):
    csvFile = open("csv_casino/casino_" + nom_mag + ".csv", "w", newline='', encoding="utf-8")
    csvWriter = csv.writer(csvFile, delimiter=';', quotechar='"')
    # -- Création du nom des colonnes --
    csvWriter.writerow(['categorie', 'type', 'nom', 'poids', 'prix_par_kg', 'prix', 'promo'])

    for i in range(1, nbr_produits+1):
        print(i)
        csv_fill = []
        get_cat_name = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/article/div[1]/div/div/span").text
        csv_fill.append(get_cat_name)
        csv_fill.append("null")
        get_it_name = driver.find_elements_by_xpath(
            "/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li[" + str(i) + "]/section/div[2]/a")
        for element in get_it_name:
            csv_fill.append(element.get_attribute('title'))
        get_it_pricekg = driver.find_elements_by_xpath(
            "/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li[" + str(i) + "]/section/div[2]/div[3]/span")
        for element in get_it_pricekg:
            try:
                strkg = re.sub("[\(\[].*?[\)\]]", "", element.text)
                strprix = re.search('\(([^)]+)', element.text).group(1)
                csv_fill.append(strkg)
                csv_fill.append(strprix)
                get_price = driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li[" + str(
                        i) + "]/section/div[2]/div[4]/div/div")
                csv_fill.append(get_price.text)
            except AttributeError:
                csv_fill.append(element.text)
                get_price = driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li[" + str(
                        i) + "]/section/div[2]/div[4]/div/div")
                csv_fill.append(get_price.text)
                csv_fill.append(get_price.text)

        try:
            get_promo = driver.find_element_by_xpath(
                "/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li[" + str(i) + "]/section/div[1]/div[2]/img")
            img_src = get_promo.get_attribute('src')
            if img_src == "https://imgart.casino.fr/imageserver/MCL/images/promo/picto_promo_T1.png" or img_src == "//imgart.casino.fr/imageserver/MCL/images/promo/Zerm_T1.png":
                csv_fill.append("oui")

            else:
                csv_fill.append("non")

        except WebDriverException:
            csv_fill.append("non")
        csvWriter.writerow((csv_fill))

#                                       SELECTIONS DRIVE
Openheader()
GetLinkShop()
