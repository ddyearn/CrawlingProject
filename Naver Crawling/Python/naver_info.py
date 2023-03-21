from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
import csv

# 제품 상세 : 상품명/상품번호/판매원가/판매할인가/할인률/배송비/리뷰수/별점/브랜드/카테고리/리뷰
options = webdriver.ChromeOptions()
options.add_argument('--headless')
UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://brand.naver.com/cheiljedang/products/6042668419?n_media=11068&n_rank=1&n_ad_")
time.sleep(10)

# html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("naver_info.html", "w")
f.write(soup.prettify())
f.close()

info = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset')

item = info.find_element(By.CLASS_NAME, '_22kNQuEXmb').text
itemId = driver.find_element(By.CLASS_NAME, 'ABROiEshTD').text
price = info.find_element(By.CLASS_NAME, 'Xdhdpm0BD9').text
discountPrice = info.find_element(By.CLASS_NAME, 'aICRqgP9zw').text
discountRate = info.find_element(By.CLASS_NAME, '_1G-IvlyANt').text
delivery = info.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1rGSKv6aq_ > div > span:nth-child(2)').text
reviewCount = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv > div:nth-child(1) > a > strong').text
starscore = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv > div:nth-child(2) > strong').text
brandname = driver.find_element(By.CLASS_NAME, 'KasFrJs3SA').text
category = driver.find_element(By.CLASS_NAME, '_3bYOrjr_7d').text

f = open('./Naver_Item_Info.csv', 'w', newline='')
wr = csv.writer(f)
wr.writerow(['상품명', item])
wr.writerow(['상품번호', itemId])
wr.writerow(['판매원가', price])
wr.writerow(['판매할인가', discountPrice])
wr.writerow(['할인률',discountRate])
wr.writerow(['배송비',delivery])
wr.writerow(['리뷰수',reviewCount])
wr.writerow(['별점',starscore])
wr.writerow(['브랜드',brandname])
wr.writerow(['카테고리',category])
f.close()

cidList = []
rstarList = []
contentList = []

driver.find_element(By.CLASS_NAME, '_11xjFby3Le').click()
reviews = driver.find_elements(By.CLASS_NAME, '_2389dRohZq')
for review in reviews:
    cid = review.find_element(By.TAG_NAME, 'strong').text
    rstar = review.find_element(By.CLASS_NAME, '_15NU42F3kT').text
    content = review.find_element(By.CLASS_NAME, 'YEtwtZFLDz').text

    cidList.append(cid)
    rstarList.append(rstar)
    contentList.append(content)

dic = {'reviewer' : cidList, 'star rate' : rstarList, 'review' : contentList}
Naver_Review_df = pd.DataFrame(dic)
Naver_Review_df.to_csv('./Naver_Review.csv')

driver.quit()