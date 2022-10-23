import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#
# # rightmove web scrapper
url = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=1&maxPrice=1750&minPrice=1500&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="
newset = set()
x = requests.get(url)

soup = BeautifulSoup(x.text, 'html.parser')
for link in soup.find_all('div', class_="propertyCard-details"):
    newset.add(link.find(class_="propertyCard-link").find(class_="propertyCard-address").find("meta")["content"])

# try next pages
index = 0

url_next_page = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=1&maxPrice=1750&minPrice=1500&index={}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=".format(
    index)
x = requests.get(url_next_page)

while x.status_code == 200:
    soup = BeautifulSoup(x.text, 'html.parser')
    for link in soup.find_all('div', class_="propertyCard-details"):
        newitem = link.find(class_="propertyCard-link").find(class_="propertyCard-address").find("meta")["content"]
        if newitem != "":
            newset.add(newitem)

    index += 24
    url_next_page = "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=1&maxPrice=1750&minPrice=1500&index={}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=".format(
        index)
    x = requests.get(url_next_page)

print ("rightmove scraper finished")

# zoopla web scrapper

newset2 = set()
url = "https://www.zoopla.co.uk/to-rent/property/london/?price_frequency=per_month&q=London&search_source=refine&price_max=1600&price_min=1000"

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get(url)
WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"#gdpr-consent-notice")))
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-theme/div/div/app-notice/app-theme/div/div/app-home/div/div[2]/app-footer/div/div[2]/app-action-buttons/div/button[2]"))).click()


newtest = driver.find_elements(By.XPATH,"/html/body/div[3]/div/main/div/div[3]/div[2]/section/div[2]/div[2]/*/div/div/div/div[2]/a/div/div[3]/h3")
for item in newtest:
    newset2.add(item.text)


newindex = 1
url2 = "https://www.zoopla.co.uk/to-rent/property/london/?price_frequency=per_month&q=London&search_source=refine&price_max=1600&price_min=1000"

driver.get(url2)
newtest2 = driver.find_elements(By.XPATH, "/html/body/div[3]/div/main/div/div[3]/div[2]/section/div[2]/div[2]/*/div/div/div/div[2]/a/div/div[3]/h3")
for item2 in newtest2:
    newset2.add(item2.text)

while len(newtest2) != 0:

    newindex += 1
    url2 = "https://www.zoopla.co.uk/to-rent/property/london/?price_frequency=per_month&q=London&search_source=refine&price_max=1600&price_min=1000&pn={}".format(newindex)
    driver.get(url2)
    newtest2 = driver.find_elements(By.XPATH, "/html/body/div[3]/div/main/div/div[3]/div[2]/section/div[2]/div[2]/*/div/div/div/div[2]/a/div/div[3]/h3")
    for item2 in newtest2:
        newset2.add(item2.text)


print ("zoopla scrapper finished")

z = newset.union(newset2)

print("the intersection", z)