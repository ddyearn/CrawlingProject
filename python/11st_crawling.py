from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime

# 브라우저 자동종료 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 브라우저 생성
browser = webdriver.Chrome('./chromedriver', options=chrome_options)

# 웹사이트 열기
browser.get('https://www.11st.co.kr/main')

'''
# 로그인 페이지로 넘어가기
browser.implicitly_wait(5)
browser.find_element(By.CSS_SELECTOR, "#gnb_login_button > span.gnb_txt").click()

# 아이디 입력
id = browser.find_element(By.CSS_SELECTOR, "#id")
id.click()
id.send_keys("bestsy3785")

# 비밀번호 입력
pw = browser.find_element(By.CSS_SELECTOR, "#pw")
pw.click()
pw.send_keys("sherry4869")

# 로그인
browser.implicitly_wait(3)
login_btn = browser.find_element(By.CSS_SELECTOR, "#log\.login")
login_btn.click()
'''

# 베스트
browser.find_element(By.CSS_SELECTOR, "#gnb > div > div.b_header_util > div > div.c_util_servicelink > ul:nth-child(2) > li.line > a").click()

# 스크롤 함수  (속도가 느림)
def doScrollDown(whileSeconds):
	start = datetime.datetime.now()
	end = start + datetime.timedelta(seconds=whileSeconds)
	while True:
		browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		time.sleep(1)
		if datetime.datetime.now() > end:
			break


doScrollDown(20)

# 데이터 저장 파일 열기
f = open("11st_crawling.txt", "w")

# 아이템 리스트 가져오기

items = browser.find_elements(By.CLASS_NAME, "ranking_pd")
for item in items:
	info = item.find_element(By.TAG_NAME, 'a')
	title = info.find_element(By.TAG_NAME, 'p').text
	url = info.get_attribute('href')
	#price = info.find_element(By.CLASS_NAME, "normal_price").text
	#sale_price = info.find_element(By.CLASS_NAME, "sale_price").text 
	#" | " + price + " | " + sale_price + 
	# file 쓰기
	f.write(title + " | " + url + "\n")

f.close()
browser.close()
