from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random as rd
import dropbox
import datetime
import base64
import os
import schedule


def job():
  try:

    dbx_token = os.environ.get("dbx_token")
    dbx = dropbox.Dropbox(dbx_token)

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
    wd = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=options)
    
    #wd.get("https://www.google.com")
    #print(wd.page_source)
    
    wd.get('https://instagram.com')
    time.sleep(rd.uniform(9,11))

    username = os.environ.get("INSTAGRAM_USER")
    password = os.environ.get("INSTAGRAM_PASSWORD")

    time.sleep(rd.uniform(2.5,3.5))
    # wd.find_element_by_name('username').send_keys(username)
    # WebDriverWait(wd, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))).send_keys(username)
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(username)
    print("Username entered")
    # wd.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
    time.sleep(rd.uniform(0.95,1.45))
    # wd.find_element_by_name('password').send_keys(password + Keys.ENTER)
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(password)
    print("Password entered")
    time.sleep(rd.uniform(0.95,1.45))

    S = lambda X: wd.execute_script('return document.body.parentNode.scroll' + X)
    wd.set_window_size(S('Width'), S('Height'))
    image_code = wd.find_element_by_tag_name('body').screenshot_as_base64
    dbx.files_upload(base64.decodebytes(image_code.encode()), "/TEXT/" + "page_after_input" + datetime.datetime.today().strftime("_%d.%m.%Y_%H:%M:%S") + ".png", mute = True)
    print("Screenshot 1 has been processed")
    time.sleep(rd.uniform(4.5,5.5))


    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()
    time.sleep(rd.uniform(6,8))
    print("Submit button's been clicked")

    S = lambda X: wd.execute_script('return document.body.parentNode.scroll' + X)
    wd.set_window_size(S('Width'), S('Height'))
    image_code = wd.find_element_by_tag_name('body').screenshot_as_base64
    dbx.files_upload(base64.decodebytes(image_code.encode()), "/TEXT/" + "page_after_login" + datetime.datetime.today().strftime("_%d.%m.%Y_%H:%M:%S") + ".png", mute = True)
    print("Screenshot 2 has been processed")
    time.sleep(rd.uniform(4.5,5.5))

    # wd.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
    #time.sleep(rd.uniform(0.95,1.45))
    # wd.find_element_by_xpath('//button[@type="submit"]').click()

    wd.get('https://www.instagram.com/')
    time.sleep(rd.uniform(4.5,5.5))
    print("The webpage 'https://www.instagram.com/' has been opened")

    S = lambda X: wd.execute_script('return document.body.parentNode.scroll' + X)
    wd.set_window_size(S('Width'), S('Height'))
    image_code = wd.find_element_by_tag_name('body').screenshot_as_base64
    dbx.files_upload(base64.decodebytes(image_code.encode()), "/TEXT/" + "main_page" + datetime.datetime.today().strftime("_%d.%m.%Y_%H:%M:%S") + ".png", mute = True)
    print("Screenshot 3 has been processed")

    time.sleep(rd.uniform(2.5,3.5))
    
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]"))).click()
    # wd.find_element_by_xpath("//button[contains(text(), 'Не сейчас')]").click()

    S = lambda X: wd.execute_script('return document.body.parentNode.scroll' + X)
    wd.set_window_size(S('Width'), S('Height'))
    image_code = wd.find_element_by_tag_name('body').screenshot_as_base64
    dbx.files_upload(base64.decodebytes(image_code.encode()), "/TEXT/" + "page_after_clicking_not_now" + datetime.datetime.today().strftime("_%d.%m.%Y_%H:%M:%S") + ".png", mute = True)
    print("Screenshot 4 has been processed")
    
    print("The 'Not Now' button has been clicked")
    time.sleep(rd.uniform(2.5,3.5))
    wd.find_element_by_class_name('Ckrof').click()
    time.sleep(rd.uniform(1.5,2.5))
    print("SUCCESS")

    wd.quit()
  except Exception as e:
    print(e)


schedule.every(5).minutes.do(job)


while True:
  schedule.run_pending()
  time.sleep(10)