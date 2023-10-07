import pytest
from contextlib import nullcontext as does_not_raise
import requests

from laundry_booker.laundry_booker import Booker


class TestClass:
    instance = Booker()

    @pytest.mark.parametrize("uri,expectation", [("https://github.com/____", pytest.raises(requests.exceptions.HTTPError)), ("https://gitxxxxxhub.com/", pytest.raises(requests.exceptions.ConnectionError)), ("https://github.com/", does_not_raise()), ("https://ilmarinen.visiontech.fi/Default.aspx", does_not_raise())])
    def test_url_connect(self, uri, expectation):
        with expectation:
            self.instance.open_uri(uri)
    
    
    
