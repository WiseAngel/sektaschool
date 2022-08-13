import os
from datetime import datetime
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import core.context as ctx
import utils.os_manipulation as om
import utils.resource_loader as rl
from utils.data_manipulation import get_random_string
from utils.logging import Logs

BROWSERS = ["chrome", "headlesschrome", "firefox", "opera"]
ENVS = ["dev", "test", "prod"]
LOGGING_TYPE = ["off", "fail", "all"]


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser")
    user_agent = request.config.getoption("user_agent")
    logging = request.config.getoption("logging")
    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    browser = None
    folder_download = om.add_new_directory(ctx.DOWNLOAD_FOLDER)  # TODO
    preferences = {
        "download.default_directory": folder_download,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    if logging not in LOGGING_TYPE:
        raise pytest.UsageError(
            f"--logging should be one of: {', '.join(LOGGING_TYPE)}")

    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        options = Options()
        options.add_argument(f"--user-agent=\"{user_agent}\"")
        options.add_argument("--force-device-scale-factor=1")
        options.add_experimental_option("prefs", preferences)
        browser = webdriver.Chrome(
            options=options, desired_capabilities=capabilities)
    elif browser_name == "headlesschrome":
        print("\nstart headless chrome browser for test..")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--force-device-scale-factor=1")
        options.add_experimental_option("prefs", preferences)
        options.add_argument(f"--user-agent=\"{user_agent}\"")
        browser = webdriver.Chrome(
            options=options, desired_capabilities=capabilities)
    elif browser_name == "firefox" or browser_name == "ff":
        print("\nstart firefox browser for test..")
        fp = webdriver.FirefoxProfile()
        browser = webdriver.Firefox(firefox_profile=fp)
    elif browser_name == "opera":
        print("\nstart opera browser for test..")
        browser = webdriver.Opera()
    else:
        raise pytest.UsageError(
            f"--browser should be one of: {', '.join(BROWSERS)}, not {browser_name}")
    browser.set_window_size(1600, 870)
    try:
        yield browser

        root_path = os.path.dirname(os.path.dirname(__file__))
        path_to_logs_dir = os.path.join(root_path, "logs")
        Path(path_to_logs_dir).mkdir(parents=True, exist_ok=True)
        now = datetime.now()
        now_logs = now.strftime("%H%M%S")
        now_screen = now.strftime("%Y-%m-%d_%H-%M-%S")
        log_name = request.node.name.replace(
            " ", "").encode("utf-8").decode("unicode-escape")
        failed = request.node.rep_setup.failed or request.node.rep_call.failed
        store_logs = logging == "all" or (logging == "fail" and failed)

        if store_logs:
            result = "FAILED" if failed else "PASSED"
            file_name = f"{result}_{now_logs}_{log_name}.json"
            Logs.get_network_logs(browser, path_to_logs_dir, file_name)
            Logs.get_browser_logs(browser, path_to_logs_dir, file_name)
            Logs.get_performance_logs(browser, path_to_logs_dir, file_name)

        if request.node.rep_setup.passed or request.node.rep_call.failed or request.node.rep_call.skipped or request.node.rep_setup.failed:
            attach_name = request.function.__name__ + "_" + now_screen
            allure.attach(
                browser.get_screenshot_as_png(),
                name=attach_name,
                attachment_type=allure.attachment_type.PNG
            )
    finally:
        om.delete_files_of_directory()
        om.delete_directory(folder_download)
        print("\nquit browser..")
        browser.quit()


@pytest.fixture(scope="function")
def browser_name(request):
    return request.config.getoption("browser").lower()


@pytest.fixture(scope="function")
def delete_files():
    yield
    om.delete_files_of_directory()


@pytest.fixture(scope="session")
def env(request):
    env = request.config.getoption("env").lower()
    if env not in ENVS:
        raise pytest.UsageError(f"--env should be one of: {', '.join(ENVS)}")
    return env


@pytest.fixture(scope="class")
def get_test_data():

    def _get_test_data(resource_name):
        return rl.get_test_data(resource_name)

    yield _get_test_data


@pytest.fixture(scope="class")
def get_root_test_data():

    def _get_test_data(resource_name):
        return rl.get_test_data(resource_name)

    yield _get_test_data


@pytest.fixture(scope="session", autouse=True)
def init_context(env):
    ctx.USERS = rl.get_environment_resource("users.json")[env]
    ctx.URLS = rl.get_environment_resource("urls.json")[env]
    ctx.DOWNLOAD_FOLDER = f"{rl.get_environment_resource('download_options.json')['download_folder']}_{get_random_string()}"


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Choose browser")
    parser.addoption("--env", action="store", default="dev",
                     help="Choose environment")
    parser.addoption("--user_agent", action="store", default="autotests",
                     help="Choose user-agent")
    parser.addoption("--logging", action="store", default="off",
                     help="Choose logging method")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_time():
    start = datetime.now()
    with allure.step(f"Тест запущен в: {start.strftime('%H:%M:%S')}"):
        pass
    yield
    end = datetime.now()
    with allure.step(f"Тест завершен в: {end.strftime('%H:%M:%S')}"):
        pass


@pytest.fixture(scope="function")
def user_agent(request):
    return request.config.getoption("user_agent").lower()
