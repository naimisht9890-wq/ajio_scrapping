import time
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome()
driver.get("https://www.google.com")
time.sleep(10)
user_input=driver.find_element(by=By.NAME,value='q')
user_input.send_keys("Teknowell EduTech")
time.sleep(5)
user_input.send_keys(Keys.ENTER)
time.sleep(20)
link=driver.find_element(By.XPATH,value=
driver.quit()
