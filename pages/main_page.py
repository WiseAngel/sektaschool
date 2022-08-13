import allure
import core.context as ctx
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BaseLocators, BasePage


class MainPage(BasePage):
    def __init__(self, browser: WebDriver, need_open=True, need_check=True):
        super(MainPage, self).__init__(
            browser, ctx.URLS, need_open, need_check)

    @allure.step("Проверяем открыта ли главная страница сайта")
    def _is_opened(self):
        self.wait_until_header_logo_present()

    @allure.step("Получаем видимость логотипа в header-menu")
    def is_header_logo_visible(self):
        return self._is_visible(MainPageLocators.header_logo())

    @allure.step("Ожидаем наличия логотипа в header-menu")
    def wait_until_header_logo_present(self):
        self.wait_until_present(MainPageLocators.header_logo(),
                                "Не отображается логотип в header-menu")


class MainPageLocators(BaseLocators):
    @classmethod
    @allure.step("Получаем локатор логотипа в header-menu")
    def header_logo(cls):
        header_container = cls.add_child(cls.HEADER.value, cls.CONTAINER.value)
        header_logo = cls.append_text_to_locator(
            cls.TAG_A.value, "[aria-current='page']")
        return cls.add_child(header_container, header_logo)

    CONTAINER = (By.CSS_SELECTOR, ".container")
    HEADER = (By.CSS_SELECTOR, "header")
    TAG_A = (By.CSS_SELECTOR, "a")


class MainPageHelper:
    @staticmethod
    @allure.step("Example")
    def example(page: MainPage):
        pass
