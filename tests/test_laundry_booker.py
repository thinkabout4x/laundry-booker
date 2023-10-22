import pytest
from contextlib import nullcontext as does_not_raise
import requests
from selenium.common.exceptions import TimeoutException

from laundry_booker.laundry_booker import Booker
from laundry_booker.user_handler import UserHandler,User

userhandler = UserHandler(15)

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

    
