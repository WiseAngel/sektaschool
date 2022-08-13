import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

default_timeout = 10
default_poll = 0.5


def until(method, message, timeout=default_timeout):
    """Calls the method until the return value is not False."""
    end_time = time.time() + timeout
    while True:
        value = method()
        if value:
            return
        time.sleep(default_poll)
        if time.time() > end_time:
            break
    raise TimeoutException(message)


def until_not(method, message, timeout=default_timeout):
    """Calls the method until the return value is False."""
    end_time = time.time() + timeout
    while True:
        value = method()
        if not value:
            return
        time.sleep(default_poll)
        if time.time() > end_time:
            break
    raise TimeoutException(message)


def until_ec(browser: WebDriver, ec: EC, message: str, timeout=default_timeout, poll=default_poll):
    WebDriverWait(browser, timeout=timeout, poll_frequency=poll).until(ec, message=message)


def until_not_ec(browser: WebDriver, ec: EC, message: str, timeout=default_timeout):
    WebDriverWait(browser, timeout=timeout, poll_frequency=default_poll).until_not(ec, message=message)
