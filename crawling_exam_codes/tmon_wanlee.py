from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

#import pandas as pd
import time

print("Start..")
driver = wb.Chrome( 'chromedriver' )

driver.get(url="https://search.tmon.co.kr/search/?keyword=크리넥스&thr=hs")
time.sleep(1)
#link = driver.find_elements(By.CSS_SELECTOR, "#search_app > div.ct_wrap > section.search_deallist > div.deallist_wrap > ul > li:nth-child(2) > a > div.deal_info > p > strong")
#print( link )
soup = bs(driver.page_source, "lxml")

print("First Page Download Completed...")
with open("firstpage_tmon.html", "w", encoding = 'utf-8') as file:
    file.write( str(soup.prettify()) )

print("First Page Storing Completed...")
title = soup.select("strong.tx")
price = soup.select("span.price")
#title = soup.select_one("strong.tx")
#price = soup.select_one("i.num")

for i in range(5):
    print( title[i] )
    print( price[i] )

print( "End of Analysis" )
#driver.close()


