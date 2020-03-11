from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import wget
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
file = open('videolink.txt','r')
chrome_options = Options()
chrome_options.add_argument("--headless")
for cur_link in file:
    link = cur_link
    driver = webdriver.Chrome(options = chrome_options)
    driver.get('https://www.savethevideo.com/')
    driver.find_element_by_id("url").send_keys(link)
    #js = "document.getElementById('page_size').options[1].text = '100';"
    #driver.find_element_by_id("url").send_keys(Keys.ENTER)
    driver.implicitly_wait(15)
    #driver.execute_script("window.scrollTo(0, Y)")
    links = driver.find_elements_by_class_name('is-clipped')
    first_link = None
    for i in links:
        if "player" in i.text:
            first_link = i.text.split()[1]
            break
    print(first_link)
    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get('https://www.savethevideo.com/')
    driver.find_element_by_id("url").send_keys(first_link)
    #driver.find_element_by_id("url").send_keys('https://www.allrecipes.com/video/2836/slow-cooker-carnitas/')
    driver.implicitly_wait(150)
    driver.find_element_by_id("url").send_keys(Keys.ENTER)
    timeout = 20
    # Explicitly wait 20 seconds for the element to exist.
    # Good place to put a try/except block in case of timeout.
    try:
        element = driver.find_element_by_class_name('check')
        elem = WebDriverWait(driver,timeout).until(EC.visibility_of(element))
        #elem = WebDriverWait(driver, timeout).until(EC.visibility_of((By.CLASS_NAME,'check')))
    except NoSuchElementException:
        element = None
    #driver.execute_script("window.scrollTo(0, Y)")
    links = driver.find_elements_by_tag_name('a')
    final_link = None
    for i in links:
        if i.get_attribute('href') == None:
            continue
        if "save" not in (i.get_attribute('href')) and "videoproc" not in i.get_attribute('href'):
            final_link = i.get_attribute('href')
            break
    print(final_link)
    file_name = cur_link.split('/')[-2]
    print(file_name)
    wget.download(final_link,out=file_name+'.mp4')
