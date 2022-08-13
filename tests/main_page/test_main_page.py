import allure
import pytest
import utils.assert_utils as _assert
from pages.main_page import MainPage


@pytest.mark.xdist_group("main")
@allure.parent_suite("Главная страница")
@allure.suite("Главная страница")
@allure.sub_suite("Главная страница")
@allure.label("Никита Свечкарёв")
class TestMainPage:
    @allure.title("Вёрстка главной страницы")
    def test_main_page(self, browser):
        # Arrange
        main_page = MainPage(browser)

        # Act
        main_page.wait_until_header_logo_present()

        # Assert
        _assert.wait_true(main_page.is_header_logo_visible,
                          "отображается логотип",
                          "Не отображается логотип")
