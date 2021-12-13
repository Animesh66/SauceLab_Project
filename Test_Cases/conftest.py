import os
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from webdriver_manager.firefox import GeckoDriverManager
from Utilities.utils_config_reader import configuration_reader


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def log_on_failure(request, get_browser):
    yield
    item = request.node
    driver = get_browser
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="do_login", attachment_type=AttachmentType.PNG)


# @pytest.fixture(params=["firefox", "chrome", ], scope="function")
# def get_browser(request):
#     if request.param == "chrome":
#         driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
#     if request.param == "firefox":
#         driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
#     request.cls.driver = driver
#     driver.get(configuration_reader("basic configuration", "test_url"))
#     driver.maximize_window()
#     driver.implicitly_wait(10)
#     yield driver
#     driver.quit()

@pytest.fixture(params=["firefox", "chrome"], scope="function")
def get_browser(request):
    user_name = os.getenv("SAUCE_USERNAME")
    access_key = os.getenv("SAUCE_ACCESS_KEY")
    sauce_url = "https://{}:{}@ondemand.eu-central-1.saucelabs.com:443/wd/hub".format(user_name,access_key)
    desired_cap = {}
    sauce_options = {
        'platformName': 'Windows 10',
        'browserVersion': 'latest',
        'name': request.node.name,
        'capturePerformance': True,
        'extendedDebugging': True
    }
    if request.param == "chrome":
        desired_cap['browserName'] = 'chrome'
        desired_cap['sauce:options'] = sauce_options
        driver = webdriver.Remote(sauce_url, desired_capabilities=desired_cap)
    elif request.param == "firefox":
        desired_cap['browserName'] = 'firefox'
        desired_cap['sauce:options'] = sauce_options
        driver = webdriver.Remote(sauce_url, desired_capabilities=desired_cap)
    request.cls.driver = driver
    driver.get(configuration_reader("basic configuration", "test_url"))
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.execute_script("sauce:job-result=passed")
    driver.quit()
