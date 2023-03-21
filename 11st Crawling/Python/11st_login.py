from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
import pyperclip


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('lang=ko_KR')
# options.add_argument("--window-size=10, 200")
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 웹사이트 열기
driver.get('https://www.11st.co.kr/main')

# 로그인 페이지로 넘어가기
driver.implicitly_wait(5)
driver.find_element(By.CSS_SELECTOR, "#gnb > div > div.b_header_util > div > div.c_util_etc > div.group.login_status > a:nth-child(1)").click()
time.sleep(2)

# 아이디 입력
id = driver.find_element(By.CSS_SELECTOR, "#memId")
id.click()
id.send_keys("bestsy3785")
time.sleep(2)

# 비밀번호 입력
pw = driver.find_element(By.CSS_SELECTOR, "#memPwd")
pw.click()
pw.send_keys("sherry4869")
time.sleep(2)

# 로그인
driver.implicitly_wait(3)
login_btn = driver.find_element(By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > form > fieldset > div.c-buttons > button")
login_btn.click()
time.sleep(2)

# 간편 로그인 등록 안내
driver.find_element(By.XPATH, '//*[@id="arModalQuickInfo"]/div/div/div[4]/a').click()
time.sleep(5)


# 데이터 저장 파일 열기
f = open("11st.html", "w")
f.write(driver.page_source)
f.close()

# 브라우저 종료
# browser.close() # 현재 탭만 종료
driver.quit() # 전체 브라우저 종료
