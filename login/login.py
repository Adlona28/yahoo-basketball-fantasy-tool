import os
import yaml
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def _current_directory():
    return os.path.dirname(os.path.abspath(__file__))

def _loadSettings():
    
    file_path = os.path.join(os.path.dirname(_current_directory()), 
                    os.path.join('configuration', 'settings.yaml'))
    
    with open(file_path, 'r') as stream:    
        settings = yaml.load(stream, Loader=yaml.FullLoader)
        
    return settings

def _accessWebsite():
    
    WEBSITE_URL = 'https://login.yahoo.com/'
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get(WEBSITE_URL)
    time.sleep(2)
    
    return driver

def _inputUsername(driver, userName):

    usernameBox = driver.find_element_by_name("username")
    usernameBox.send_keys(userName)
    driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)
    time.sleep(2)

def _inputPassword(driver, password):

    try:
        passwordBox = driver.find_element_by_name("password")
        passwordBox.send_keys(settings['password'])
        driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)

    except:
        print("I can't find the password box, please, resolve captcha")
        input('Press Enter to continue after resolving captcha.\n')
        password = driver.find_element_by_name("password")
        password.send_keys(settings['password'])
        driver.find_element_by_id("login-signin").send_keys(Keys.RETURN)

def login():

    settings = _loadSettings()
    driver = _accessWebsite()
    _inputUsername(driver, settings['user'])
    _inputPassword(driver, settings['password'])

if __name__ == "__main__":
    login()