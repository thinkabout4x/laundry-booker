from selenium import webdriver
import selenium.webdriver.firefox.service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import webdriver_manager.firefox

import requests


def create_firefox_options():
    """Create a firefox profile that saves downloads to directory
    """
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("-headless")
    firefox_options.set_preference('devtools.console.stdout.content', True)
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
    return firefox_options

def create_firefox_driver():
        browser = webdriver_manager.firefox.GeckoDriverManager().install() 
        firefox_options = create_firefox_options()
        driver = webdriver.Firefox(
            service=selenium.webdriver.firefox.service.Service(browser),
            options=firefox_options,
        )
        return driver

    

class Booker:
    def __init__(self, timeout_delay = 1):
        self.driver = create_firefox_driver()
        self.timeout = timeout_delay

    def open_url(self,uri):

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
            WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.ID, 'wrapper')))
        except TimeoutException:
            print("URL cant be opened")

    




