from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from dataclasses import dataclass
import requests

def verify_page_open(driver, timeout, condition, errormsg):
    """Verify that web page openes correctly, if not throws timeout exception"""
    try:
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

def create_chrome_options(headless):
    """Create a chrome profile that saves downloads to directory
    """
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("-headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    return chrome_options

def create_firefox_driver(headless):
        """Create firefox driver """
        firefox_options = create_firefox_options(headless)
        driver = webdriver.Firefox(
            options=firefox_options,
        )
        return driver

def create_chrome_driver(headless):
        """Create chrome driver """
        chrome_options = create_chrome_options(headless)
        driver = webdriver.Chrome(
            options=chrome_options,
        )
        return driver

@dataclass
class Result():
    '''class to represent result of booking'''
    # booking state
    isbooked: bool
    # day of booking
    day: str
    # time of booking
    time: str

class Booker:
    def __init__(self, user, timeout_delay = 5, headless = True, isfirefox = True):
        if isfirefox:
            self.driver = create_firefox_driver(headless)
        else:
            self.driver = create_chrome_driver(headless)
        self.timeout = timeout_delay
        self.user = user

    def open_uri(self):
        """Method to open uri"""
        try:
            with requests.head(self.user.uri) as response:
                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError:
                    print(f'Url is not valid, status code: {response.status_code}')
                    raise
        except requests.exceptions.ConnectionError as e:
            print(f'URL cant be opened, connection error, {e}')
            raise

        self.driver.get(self.user.uri)
         # Wait for the element with the ID
        verify_page_open(self.driver,self.timeout, EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_btOK")), 'URL cant be opened, timeout')

    def login(self):
        """Method to login to web page"""
        self.open_uri()
        self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_tbUsername").send_keys(self.user.login)
        self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_tbPassword").send_keys(self.user.password)
        self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btOK").click()

        verify_page_open(self.driver,self.timeout, EC.element_to_be_clickable((By.ID, 'ctl00_LinkBooking')), 'Cant login')
        # Wait for the page to load (booking button should be clickable)

    def check(self) -> bool:
        """Method to check availability of the laundry, by default looks for earliest time"""
        self.login()
        self.driver.find_element(By.LINK_TEXT, "Varaa").click()
        # Wait for the page to load (Pesula button should be clickable)
        verify_page_open(self.driver,self.timeout, EC.element_to_be_clickable((By.LINK_TEXT, "Pesula")), 'Cant go to booking choices')
        
        self.driver.find_element(By.LINK_TEXT, "Pesula").click()
        # Wait for the page to load (table for booking should be visible)
        verify_page_open(self.driver,self.timeout, EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_infostatus")), 'Cant go to laundry booking table')

        #Run through table to look for apropriate time, using id of the element
        content_id_base = "//*[@id=\"ctl00_ContentPlaceHolder1_"

        # make time equal to format on site
        target_time = self.user.target_time + ' (Vapaa)'

        for i in range(7):
            for j in range(1,8):
                curr_id = content_id_base+f'{i},'+f'{j},'+'1,'+'\"]'
                element = self.driver.find_element(By.XPATH, curr_id)
                title = element.get_attribute("title")
                if target_time == title:
                    day = self.driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_lbCalendarDag'+f'{i}').get_attribute("innerHTML").replace('<br>', ' ')
                    print("Found it! Day: "+f'{day} '+title)
                    element.click()
                    return Result(True, day, self.user.target_time)
