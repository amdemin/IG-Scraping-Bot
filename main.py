from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
from collections import Counter
import os
import time
import datetime
import base64
import random as rd
import schedule
import dropbox


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

username = os.environ.get("INSTAGRAM_USER")
password = os.environ.get("INSTAGRAM_PASSWORD")


def make_screen(wd, name):
  try:
    S = lambda X: wd.execute_script('return document.body.parentNode.scroll' + X)
    wd.set_window_size(S('Width'), S('Height'))
    image_code = wd.find_element_by_tag_name('body').screenshot_as_base64
    dbx.files_upload(base64.decodebytes(image_code.encode()), "/TEXT/" + name + datetime.datetime.today().strftime("_%d.%m.%Y_%H:%M:%S") + ".png", mute = True)
    return None
  except Exception as e:
    print("Something goes wrong making a screenshot", e)
    return None

def authorise(wd):
  try:
    wd.get('https://instagram.com')
    time.sleep(rd.uniform(8, 10))

    # wd.find_element_by_name('username').send_keys(username)
    # wd.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
    # WebDriverWait(wd, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))).send_keys(username)
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(username)
    print("Username entered")
    time.sleep(rd.uniform(0.95,1.45))
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(password)
    print("Password entered")
    time.sleep(rd.uniform(0.95,1.45))

    make_screen(wd=wd, name="page before login")
    print("Screenshot before login has been made")
    time.sleep(rd.uniform(4.5,5.5))

    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))).click()
    print("Submit button's been clicked")
    time.sleep(rd.uniform(6,8))

    make_screen(wd=wd, name="page after login")
    print("Screenshot after login has been made")
    return wd

  except Exception as e:
    print("Something goes wrong with username and password autorisation", e)
    return None

def verify_sms(wd):
  try:
    sms_verification = False
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send Security Code')]"))).click()
    time.sleep(rd.uniform(4.5,5.5))

    make_screen(wd=wd, name="SMS step 1")
    print("Screenshot SMS Verification 1 has been made")

    sms_verification = True
    waiting_minutes = round(rd.uniform(180, 240) // 60)

    # send message to my phone number about necessary sms verification
    twilio_msg = "Your Instagram Bot requires verification, please enter the code during " + str(waiting_minutes) + " minutes!"
    client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
    client.messages.create(to=os.environ.get("TWILIO_MY_PHONE"),from_=os.environ.get("TWILIO_FAKE_PHONE"),body=twilio_msg)
    
    time.sleep(waiting_minutes * 60)
    # get code from name of file stored in Code dropbox folder
    for entry in dbx.files_list_folder('/Code').entries:
      code = entry.name.strip('.txt')
    print("The SMS code is:", code)
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='security_code']"))).send_keys(code)
    time.sleep(rd.uniform(4.5,5.5))

    make_screen(wd=wd, name="SMS step 2")
    print("Screenshot SMS Verification 2 has been made")

    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))).click()
    time.sleep(rd.uniform(4.5,5.5))

    make_screen(wd=wd, name="SMS step 3")
    print("Screenshot SMS Verification 3 has been processed")
    return wd

  except Exception as e:
    if sms_verification is False:
      print("SMS verification is not needed")
      return wd
    else:
      print("Something goes wrong with SMS verification", e)
    return None

def count_story(wd, stories_dict):
  try:
    story_account = WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "FPmhX")))
    stories_dict[story_account.text] += 1
    return stories_dict
  except Exception as e:
    print("Something goes wrong with counting stories", e)
    return None

def watch_story(wd):
  try:
    # open the website
    wd.get('https://www.instagram.com/')
    time.sleep(rd.uniform(8, 10))
    print("The webpage 'https://www.instagram.com/' has been opened")

    # make the screenshot of opened main page; it should be authorised
    make_screen(wd=wd, name="Main page")
    print("Screenshot of Main Page has been made")
    time.sleep(rd.uniform(1.5, 2.5))

    # create the counter function from collections library
    stories_dict = Counter()

    # click on the story html element
    WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "Ckrof"))).click()
    time.sleep(rd.uniform(2.5,3.5))
    # count the first story
    stories_dict = count_story(wd=wd, stories_dict=stories_dict)

    # make the screenshot of the first opened story
    make_screen(wd=wd, name="Story Page")
    print("Screenshot of the first story has been made")
    time.sleep(rd.uniform(0.8,1.2))

    start = time.time()
    # the watching number of stories will be limited to 150
    for count in range(150):
      try:
          time.sleep(rd.uniform(1,1.2))
          WebDriverWait(wd, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "coreSpriteRightChevron"))).click()
          # count the current story
          time.sleep(rd.uniform(0.8,1.2))
          stories_dict = count_story(wd=wd, stories_dict=stories_dict)
      except Exception as e:
          print("CoreSpriteRightChevron is not found, perhaps stories are left", e)
          break

    end = time.time() - start
    print("Total watching time: " + str(round(end // 60)) + " m " + str(round(end % 60)) + " s ")
    print("Total number of stories:", count)
    print("The number of stories per account:", stories_dict)
    time.sleep(rd.uniform(2.5,3.5))
    return wd
  except Exception as e:
    print("Something goes wrong with watching stories", e)
    return None

def job(CHROMEDRIVER_PATH, options, username, password):
  try:
    wd = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,chrome_options=options)

    wd = authorise(wd)
    wd = verify_sms(wd)
    wd = watch_story(wd)

    wd.quit()
  except Exception as e:
    print(e)
    pass

# Schedule method will start to count each time after function's finished, it will not count time for the function execution
schedule.every(5).minutes.do(job, CHROMEDRIVER_PATH=CHROMEDRIVER_PATH, options=options, username=username, password=password)
# schedule.every(2).hours.do(job)


while True:
  schedule.run_pending()
  time.sleep(10)