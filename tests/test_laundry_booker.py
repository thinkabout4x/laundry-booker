import pytest
import os
from contextlib import nullcontext as does_not_raise
import requests
from selenium.common.exceptions import TimeoutException

from laundry_booker.laundry_booker import Booker
from laundry_booker.user_handler import UserHandler,User

userhandler = UserHandler(15)

# log and password for site
login = os.environ['login']
password = os.environ['password']

users = [User("https://ilmarinen.visiontech.fi/Default.aspx",login, password, "18:00-20:00"), User("https://github.com/____"), User("https://gitxxxxxhub.com/"), User("https://github.com/")]

for chat_id, user in enumerate(users):
    userhandler.append_user(chat_id, user)

class TestClass:

    @pytest.mark.parametrize("user,expectation", [(User("https://github.com/____"), pytest.raises(requests.exceptions.HTTPError)), (User("https://gitxxxxxhub.com/"), pytest.raises(requests.exceptions.ConnectionError)), (User("https://github.com/"), pytest.raises(TimeoutException)), (User("https://ilmarinen.visiontech.fi/Default.aspx"), does_not_raise())])
    def test_url_connect(self, user, expectation):
        instance = Booker(user)
        with expectation:
            instance.open_uri()

    @pytest.mark.parametrize("user,expectation", [(User("https://ilmarinen.visiontech.fi/Default.aspx","login", "password"), pytest.raises(TimeoutException))])
    def test_login(self, user, expectation):
        instance = Booker(user)
        with expectation:
            instance.login()

    
