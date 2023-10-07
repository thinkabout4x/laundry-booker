from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import requests


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
    def __init__(self, timeout_delay = 1, headless = True):
        self.driver = create_firefox_driver(headless)
        self.timeout = timeout_delay

    def open_uri(self,uri):

        try:
            with requests.head(uri) as response:
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    print(f'Url is not valid, status code: {response.status_code}')
                    raise
        except requests.exceptions.ConnectionError:
            print("URL cant be opened, connection error")
            raise

        self.driver.get(uri)

        try:
        # Wait for the element with the ID of wrapper
            WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.ID, 'ctl_ContentPlaceHolder1_btOK')))
        except TimeoutException:
            print("URL cant be opened")

    def login(self, uri, credentials):
        self.open_uri(uri)
        self.driver.find_element("id", "ctl00_ContentPlaceHolder1_tbUsername").send_keys(credentials[0])
        self.driver.find_element("id", "ctl00_ContentPlaceHolder1_tbPassword").send_keys(credentials[1])
        self.driver.find_element("id", "ctl00_ContentPlaceHolder1_btOK").click()



    




