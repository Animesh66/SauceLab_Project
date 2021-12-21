import pytest
from Pages.Login_Page import LoginPage
from Test_Cases.Base_Test import BaseTest
from Utilities.data_provider import get_data


class TestLogin(BaseTest):

    @pytest.mark.login_test
    @pytest.mark.parametrize("email, password", get_data("login_test"))
    def test_perform_login(self, email, password):
        login = LoginPage(self.driver)
        login.perform_login(email, password)



