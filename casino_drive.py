from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import csv
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
for i in range(2,10):
    click_croix=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(i)+"]/button/span[2]").click()
    nbr_croix=driver.find_elements_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(i)+"]//*[@class='accordion__status']")
    for j in range(1,len(nbr_croix)):
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, " + str(y) + ")")
        y+=100
        click_reg=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(i)+"]/div/div["+str(j)+"]/button/span[2]").click()
        nbr_mag=driver.find_elements_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(i)+"]/div/div["+str(j)+"]//*[@class='base-btn base-btn--primary']")
        print("g clické sur la region")
        print(len(nbr_mag))
        if(len(nbr_mag)==2):
            click_mag=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div["+str(i)+"]/div/div["+str(j)+"]/div/div/div[2]/a[2]").click()
            xpath="/html/body/div[1]/div[1]/div[4]/div/div["+str(i)+"]/div/div["+str(j)+"]/div/div/div[2]/a[2]"
        else:
            for k in range(len(nbr_mag)):
                #click_mag=driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/div[13]/div/div[1]/div/div["+str(k)+"]/div[2]/a[2]")
                xpath="/html/body/div[1]/div[1]/div[4]/div/div[13]/div/div[1]/div/div["+str(k)+"]/div[2]/a[2]"