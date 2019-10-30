from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

 
cap=webdriver.DesiredCapabilities.FIREFOX
options=Options()
options.headless= False

browser = webdriver.Firefox(capabilities=cap,options=options)

browser.get("https://www.hidemyass.com/en-gb/proxy")
iframe=browser.find_element_by_id('proxyIframe')
browser.switch_to.frame(iframe)

action=ActionChains(browser)

link=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'form_url')))
link= browser.find_element_by_id("form_url_fake")

action.move_to_element(link).click()


link.send_keys('https://video.betfair.com/')

browser.find_element_by_xpath('/html/body/form/div[2]/div[1]/input[2]').click()

browser.find_element_by_xpath('/html/body/form/div[2]/div[1]/div/div[5]').click()

button= browser.find_element_by_xpath("/html/body/form/div[3]/a")
button.click()
wait=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,'terms-agree-wrapper')))

link=browser.find_element_by_class_name('button primary')
link.click()