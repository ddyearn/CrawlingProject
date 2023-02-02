from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs

import time

print("Start..")
driver = wb.Chrome( 'chromedriver' )

driver.get(url="https://search.11st.co.kr/Search.tmall?kwd=크리넥스&fromACK=recent")
time.sleep(2)
soup = bs(driver.page_source, "lxml")

print("First Page Download Completed...")
with open("firstpage_11st.html", "w", encoding = 'utf-8') as file:
    file.write( str(soup.prettify()) )

print("First Page Storing Completed...")
title = soup.find("div", "c_prd_name c_prd_name_row_2").find("strong")
price = soup.find("span", "value")
#price = soup.find("meta", property="og:price")

print( title )
print( price )


print( "End of Analysis" )
driver.close()


