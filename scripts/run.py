from laundry_booker import booker 

# url for the site to book on
url = "https://ilmarinen.visiontech.fi/Default.aspx"
# log and password for site
credentials = ("","")
# target time for booking in 24 hour format
target_time = 18
# frequency of checking in hours
check_time_delta = 1

if __name__ == "__main__":
    instance = booker.login(url, credentials)

    instance.check(target_time, check_time_delta)

