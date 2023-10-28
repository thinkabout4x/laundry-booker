import os
from laundry_booker.laundry_booker import Booker 
from laundry_booker.user_handler import User

# url for the site to book on
uri = "https://ilmarinen.visiontech.fi/Default.aspx"
# log and password for site
login = os.environ['login']
password = os.environ['password']
# target time for booking in string format (title to find on a web page)
target_time = '20:00-21:00'

user = User(uri, login, password, target_time)

if __name__ == "__main__":
    sniffer = Booker(user, headless=False)
    sniffer.check()

