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
browser.get('https://shopping.naver.com/home')

''' 자동 로그인 막힘
# 로그인 페이지로 넘어가기
browser.implicitly_wait(5)
browser.find_element(By.CSS_SELECTOR, "#gnb_login_button > span.gnb_txt").click()

# 아이디 입력
id = browser.find_element(By.CSS_SELECTOR, "#id")
id.click()
id.send_keys("id")

# 비밀번호 입력
pw = browser.find_element(By.CSS_SELECTOR, "#pw")
pw.click()
pw.send_keys("pw")

# 로그인
browser.implicitly_wait(3)
login_btn = browser.find_element(By.CSS_SELECTOR, "#log\.login")
login_btn.click()
'''

# 검색창 클릭
browser.implicitly_wait(5)
search = browser.find_element(By.CSS_SELECTOR, "#__next > div > div.pcHeader_header__tXOY4 > div > div > div._gnb_header_area_nfFfz > div > div._gnbLogo_gnb_logo_YdOoU > div > div._gnbSearch_gnb_search_Otk5r > form > fieldset > div._gnbSearch_inner_8HZA1 > div > input")
search.click()

# 검색어 입력
search.send_keys('이소말트')
search.send_keys(Keys.ENTER)

# 스크롤 함수  (속도가 느림)
def doScrollDown(whileSeconds):
	start = datetime.datetime.now()
	end = start + datetime.timedelta(seconds=whileSeconds)
	while True:
		browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
		time.sleep(1)
		if datetime.datetime.now() > end:
			break

# 데이터 저장 파일 열기
f = open("naver_crawling.txt", "w")

# 아이템 리스트 가져오기
while True:
	doScrollDown(10)
	items = browser.find_elements(By.CLASS_NAME, "basicList_item__0T9JD")
	for item in items:
		info = item.find_element(By.CLASS_NAME, "basicList_link__JLQJf")
		title = info.get_attribute('title')
		url = info.get_attribute('href')
		price = item.find_element(By.CLASS_NAME, "price_num__S2p_v").text
		depth = item.find_element(By.CLASS_NAME, "basicList_depth__SbZWF").text
		# file 쓰기
		f.write(title + " | " + price + " | " + url + " | " + depth + "\n")
	next_btn = browser.find_element(By.CLASS_NAME, "pagination_next__pZuC6")
	if(next_btn.is_displayed()):
		next_btn.click()
	else:
		break

f.close()
'''
# 끝까지 스크롤
a = 0
while a < 500:
	a = a+1
	browser.execute_script("window.scrollTo(0, 100100100100100100100100);")
'''
