driver.get('http://www.gmarket.co.kr')

login = self._driver.find_element(By.ID, 'css_login_box')
login.click()

user_id = self._driver.find_element(By.ID, 'id')
user_id.send_keys('사용자 ID')
user_pw = self._driver.find_element(By.ID, 'pwd')
user_pw.send_keys('사용자 PW')

submit = self._driver.find_element(By.XPATH, '//div[@class="btn-login"]/a')
submit.click()
