from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

#import pandas as pd
import time

print("Start..")
driver = wb.Chrome( 'chromedriver' )

#driver.get(url="http://corners.gmarket.co.kr/Bestsellers")
#time.sleep(2)
#img = driver.find_elements(By.CSS_SELECTOR, "img.lazy")
#time.sleep(2)
#print( len(img) )

title_list = []
price_list = []

for i in range( 5 ):
    driver.get(url="http://corners.gmarket.co.kr/Bestsellers")
    img = driver.find_elements(By.CSS_SELECTOR, "img.lazy")

    print( i, "-th operation")
    img[i].click()
    time.sleep(0.5)

    #soup = bs( driver.page_source, "html")
    soup = bs(driver.page_source, "lxml")
    title = soup.select_one("h1.itemtit")
    price = soup.select_one("strong.price_real")
    title_list.append(title)
    price_list.append(price)

    driver.back()
    time.sleep(0.5)

print( title_list )
print( price_list )
driver.close()


