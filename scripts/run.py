import os
from laundry_booker.laundry_booker import Booker 

# url for the site to book on
uri = "https://ilmarinen.visiontech.fi/Default.aspx"
# log and password for site
login = os.environ['login']
password = os.environ['password']
credentials = (login,password)
# target time for booking in 24 hour format
target_time = 18
# frequency of checking in hours
check_time_delta = 1

if __name__ == "__main__":
    sniffer = Booker(uri, credentials, headless=False)
    sniffer.check()
