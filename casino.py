import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import csv
import re
#                                       SITE + COOKIES ACCEPTE
driver = webdriver.Firefox()
site = "https://www.casino.fr/prehome/courses-en-ligne/magasins"
driver.get(site)
driver.maximize_window()
button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))).click()
time.sleep(2)
list_dep1=driver.find_elements_by_xpath("//*[@class='accordion__header accordion__header--no-shadow']")
y=50
#                                       SELECTIONS DRIVE
for n in range(2,10):
    click_croix=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(n)+"]/button/span[2]").click()
    nbr_croix=driver.find_elements_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(n)+"]//*[@class='accordion__status']")
    for j in range(1,len(nbr_croix)):
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y+=100
        click_reg=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(n)+"]/div/div["+str(j)+"]/button/span[2]").click()
        nbr_mag=driver.find_elements_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(n)+"]/div/div["+str(j)+"]//*[@class='base-btn base-btn--primary']")
        x=len(nbr_mag)
        nom_mag=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div/div/div[1]/div/div[1]").text
        click_mag=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(n)+"]/div/div["+str(j)+"]/div/div/div[2]/a[2]").click()
        xpath="/html/body/div[1]/div[1]/div[4]/div/div["+str(n)+"]/div/div["+str(j)+"]/div/div/div[2]/a[2]"
        driver.find_element_by_xpath(xpath).click()
#                                       BURGER + RAYONS
        # xpath des elements dans le burger menu for i:  /html/body/div[2]/header/nav/div/ul/li[i]/div/div
        popup_close=WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[2]/div/div/div[1]/a'))).click()
        '''
        burger_menu = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/div[2]/div[3]"))).click()
        rayon = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/div"))).click()
        sous_rayon = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/ul/div/li[1]/div"))).click()
        click_rayon = WebDriverWait(driver, 100).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/ul/div/li[1]/ul/div/div/div[3]/a"))).click()
        '''



        burger_menu = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/header/div[2]/div[3]"))).click()
        rayon = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/div"))).click()
        l_sous_rayons = driver.find_elements_by_xpath("//div[@class='list-container']")
        print(len(l_sous_rayons))
        for sr in range(1,len(l_sous_rayons)):
            sous_rayon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/ul/div/li[" + str(
                        sr) + ")]/div"))).click()
            click_rayon = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[2]/header/nav/div/ul/li[4]/ul/div/li[" + str(
                        sr) + ")]/ul/div/div/div[3]/a"))).click()


        y = 1000
        for timer in range(0, 40):
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 1000
            time.sleep(1)

        #FILLING DU CSV
        # -- Création du CSV --
        csvFile = open("csv_casino/casino_"+nom_mag+".csv", "w", newline='', encoding="utf-8")
        csvWriter = csv.writer(csvFile, delimiter=';', quotechar='"')
        # -- Création du nom des colonnes --
        csvWriter.writerow(['categorie', 'type', 'nom', 'poids', 'prix_par_kg', 'prix', 'promo'])

        list_nbr_produits = driver.find_elements_by_class_name("product-item__bottom")
        print(len(list_nbr_produits))
        #list_it_name=driver.find_elements_by_class_name("product-item__description POP_open")
        y=0
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        for i in range(1, len(list_nbr_produits)):
            print(i)
            csv_fill=[]
            get_cat_name = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/article/div[1]/div/div/span").text
            csv_fill.append(get_cat_name)
            csv_fill.append("null")
            get_it_name = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li["+str(i)+"]/section/div[2]/a")
            for element in get_it_name:
                csv_fill.append(element.get_attribute('title'))
            get_it_pricekg= driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li["+str(i)+"]/section/div[2]/div[3]/span")
            for element in get_it_pricekg:
                try:
                    strkg=re.search('\(([^)]+)', element.text).group(0)
                    strprix=re.search('\(([^)]+)', element.text).group(1)
                    csv_fill.append(strkg)
                    csv_fill.append(strprix)
                except AttributeError:
                    csv_fill.append(element.text)
            get_price=driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li["+str(i)+"]/section/div[2]/div[4]/div/div")
            csv_fill.append(get_price.text)

            try:
                get_promo = driver.find_element_by_xpath(
                    "/html/body/div[2]/div[3]/div/div/article/div[3]/ul/li[" + str(i) + "]/section/div[1]/div[2]/img")
                img_src = get_promo.get_attribute('src')
                if img_src=="https://imgart.casino.fr/imageserver/MCL/images/promo/picto_promo_T1.png" or img_src=="//imgart.casino.fr/imageserver/MCL/images/promo/Zerm_T1.png":
                    csv_fill.append("oui")

                else:
                    csv_fill.append("non")

            except WebDriverException:
                csv_fill.append("non")
            csvWriter.writerow((csv_fill))

            if i==len(list_nbr_produits)-1:
                time.sleep(4)
                driver.find_element_by_xpath("/html/body/div[2]/header/div[1]/div/a[1]/span").click()
                driver.find_element_by_xpath("/html/body/div[2]/header/div[1]/div/div/ul/li[2]/a/span[2]").click()
                try:
                    burger_menu = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/div/div/div[2]/div/a[2]"))).click()
                except WebDriverException:
                     print("caca")
                pt_retrait=WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[1]/div[1]/div/div[2]/div[2]/div/a    "))).click()
#/html/body/div[2]/div[3]/div/div/article/div[1]/div/div/span








