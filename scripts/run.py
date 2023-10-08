import os
from laundry_booker.laundry_booker import Booker 

# url for the site to book on
uri = "https://ilmarinen.visiontech.fi/Default.aspx"
# log and password for site
login = os.environ['login']
password = os.environ['password']
credentials = (login,password)
# target time for booking in string format (title to find on a web page)
target_time = '20:00-21:00 (Vapaa)'
# frequency of checking in hours
check_time_delta = 1

if __name__ == "__main__":
    sniffer = Booker(uri, credentials, target_time, headless=False)
    sniffer.check()

