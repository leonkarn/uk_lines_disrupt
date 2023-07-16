import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import os


chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

# chrome_options = Options()
#chrome_options.add_argument("--remote-debugging-port=9222")
driver.get("https://lawdb.intrasoftnet.com/")
time.sleep(2)
x = driver.find_element_by_xpath("/html/body/div/div[5]/table/tbody/tr[1]/td[2]/a")
x.click()
time.sleep(2)

username = driver.find_element_by_xpath("/html/body/div/div[4]/div/div[1]/form/div[1]/input")
username.send_keys("NOM104605")

password = driver.find_element_by_xpath("/html/body/div/div[4]/div/div[1]/form/div[2]/input")
password.send_keys("09441")
time.sleep(1)

button = driver.find_element_by_xpath("/html/body/div/div[4]/div/div[1]/form/button")
button.click()
time.sleep(1)

nomos = driver.find_element_by_xpath("/html/body/div[2]/div[2]/ul/li[2]/a")
nomos.click()
time.sleep(1)

kwdikoi = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/table/tbody/tr[4]")
kwdikoi.click()
time.sleep(1)

dikoikonia = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/table/tbody/tr[2]/td/table/tbody/tr[9]")
dikoikonia.click()
time.sleep(1)

titlos1 = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/table[2]/tbody/tr/td/table/tbody/tr[2]/td[4]")
titlos1.click()
time.sleep(1)

table = driver.find_element_by_id("SCROLLTABLE")
rows = table.find_elements_by_tag_name("tr")
newdict = {}
import pandas as pd
articles = []
titles = []

for row in rows:
    columns = row.find_elements_by_tag_name("td")
    articles.append(columns[1].text)
    titles.append(columns[2].text)

d = {'αρθρα':articles, 'τιτλοι': titles}
df = pd.DataFrame(data=d)

# df.to_csv("nomoi.csv")
