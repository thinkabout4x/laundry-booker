from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import requests

def verify_page_open(driver, timeout, condition, errormsg):
    try:
    # Wait for the element with the ID
        WebDriverWait(driver, timeout).until(condition)
    except TimeoutException as e:
        print(errormsg)
        print(f'Exception: {e}')
        raise

def create_firefox_options(headless):
    """Create a firefox profile that saves downloads to directory
    """
    firefox_options = webdriver.FirefoxOptions()
    if headless:
        firefox_options.add_argument("-headless")
    firefox_options.set_preference('devtools.console.stdout.content', True)
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
    return firefox_options

def create_firefox_driver(headless):
        firefox_options = create_firefox_options(headless)
        driver = webdriver.Firefox(
            options=firefox_options,
        )
        return driver

class Booker:
    def __init__(self, uri, credentials, timeout_delay = 5, headless = True):
        self.driver = create_firefox_driver(headless)
        self.timeout = timeout_delay
        self.uri = uri
        self.credentials = credentials

    def open_uri(self):

        try:
            with requests.head(self.uri) as response:
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    print(f'Url is not valid, status code: {response.status_code}')
                    raise
        except requests.exceptions.ConnectionError as e:
            print(f'URL cant be opened, connection error, {e}')
            raise

        self.driver.get(self.uri)
         # Wait for the element with the ID
        verify_page_open(self.driver,self.timeout, EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btOK")), 'URL cant be opened, timeout')

    def login(self):
        self.open_uri()
        self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_tbUsername").send_keys(self.credentials[0])
        self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_tbPassword").send_keys(self.credentials[1])
        self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btOK").click()

        verify_page_open(self.driver,self.timeout, EC.element_to_be_clickable((By.ID, 'ctl00_LinkBooking')), 'Cant login')
        # Wait for the page to load (booking button should be clickable)

    def check(self):
        self.login()
        self.driver.find_element(By.LINK_TEXT, "Varaa").click()
        # Wait for the page to load (Pesula button should be clickable)
        verify_page_open(self.driver,self.timeout, EC.element_to_be_clickable((By.LINK_TEXT, "Pesula")), 'Cant go to booking choices')
        
        self.driver.find_element(By.LINK_TEXT, "Pesula").click()
        # Wait for the page to load (table for booking should be visible)
        verify_page_open(self.driver,self.timeout, EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_infostatus")), 'Cant go to laundry booking table')












    




