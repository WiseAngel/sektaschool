import time
from abc import ABC, abstractmethod
from enum import Enum

import allure
import utils.os_manipulation as om
import utils.wait_utils as wait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class BasePage(ABC):
    def __init__(self, browser: WebDriver, url: str, need_open=True, need_check=True):
        self._browser = browser
        self._url = url

        if need_open:
            self.open(need_check)
        elif need_check:
            self.check_is_opened()

    @allure.step("Подтверждаем алерт без текста")
    def _accept_alert(self):
        self._browser.switch_to.alert.accept()
        self.wait_until_alert_not_present("Не закрылся алерт")

    def _auto_authorize(self, token: str = None):
        # auth_token = token if token else ctx.AGELESS_TOKEN
        # self._browser.execute_script("window.localStorage.setItem('auth_token','{}')".format(auth_token))
        # print("refresh")
        self._browser.refresh()

    @allure.step("Очищаем текст элемента по локатору")
    def _clear(self, locator):
        self.wait_until_enabled(
            locator, "Элемент должен быть активен перед очисткой")
        el = self._browser.find_element(*locator)
        while el.get_property("value"):
            el.send_keys(Keys.BACK_SPACE)

    @allure.step("Кликаем на элемент по локатору")
    def _click(self, locator):
        self.wait_until_enabled(
            locator, "Элемент должен быть активен перед кликом")
        self._browser.find_element(*locator).click()

    @allure.step("Выбираем значение из выпадающего списка по индексу")
    def _select_by_index(self, locator, value):
        self.wait_until_enabled(locator, "Элемент должен быть активен")
        select = Select(self._browser.find_element(*locator))
        select.select_by_index(value)

    @allure.step("Выбираем значение из выпадающего списка по значению")
    def _select_by_value(self, locator, value):
        self.wait_until_enabled(locator, "Элемент должен быть активен")
        select = Select(self._browser.find_element(*locator))
        select.select_by_value(value)

    @allure.step("Кликаем на элемент по локатору и номеру элемента")
    def _click_by_number(self, locator, item_number: int = 1):
        self.wait_until_enabled(
            locator, "Элемент должен быть активен перед кликом")
        return self._browser.find_elements(*locator)[item_number - 1].click()

    @allure.step("Кликаем на элемент по координатам")
    def _click_element_by_coordinates(self, locator, x: int, y: int):
        ActionChains(self._browser).move_to_element(self._browser.find_element(*locator)) \
            .move_by_offset(x, y).click().perform()

    @allure.step("Кликаем на n-ный элемент по локатору")
    def _click_nth_of(self, locator, nth_child: int):
        nth_locator = BaseLocators.get_nth_child(locator, nth_child)
        self._click(nth_locator)

    @allure.step("Удалить текст в элемент по локатору без проверок")
    def _force_clear(self, locator):
        el = self._browser.find_element(*locator)
        while el.get_property("value"):
            el.send_keys(Keys.BACK_SPACE)

    @allure.step("Кликаем на элемент по локатору без проверок")
    def _force_click(self, locator):
        self._browser.find_element(*locator).click()

    @allure.step("Получаем значение аттрибута элемента по локатору без проверки")
    def _force_get_attribute(self, locator, attribute: str):
        return self._browser.find_element(*locator).get_attribute(attribute)

    @allure.step("Получаем текст элемента по локатору без проверки")
    def _force_get_text(self, locator):
        return self._browser.find_element(*locator).text

    @allure.step("Ввести текст в элемент по локатору без проверок")
    def _force_input(self, locator, text):
        self._browser.find_element(*locator).send_keys(text)

    @allure.step("Форматируем шаблон локатора параметрами")
    def _format(self, locator_tmpl: tuple, *placeholders):
        item_loc_list = list(locator_tmpl)
        item_loc_list[1] = item_loc_list[1].format(*placeholders)
        return tuple(item_loc_list)

    @allure.step("Получаем количество элементов по локатору")
    def _get_amount_element_by_locator(self, locator):
        list_elements = self._browser.find_elements(*locator)
        return len(list_elements)

    @allure.step("Получаем значение аттрибута элемента по локатору")
    def _get_attribute(self, locator, attribute: str):
        self.wait_until_enabled(
            locator, "Элемент должен быть стабилен перед получением текста")
        return self._browser.find_element(*locator).get_attribute(attribute)

    @allure.step("Получаем значение аттрибута элемента по локатору и номеру элемента")
    def _get_attribute_by_number(self, locator, attribute: str, item_number: int = 1):
        self.wait_until_enabled(
            locator, "Элемент должен быть стабилен перед получением текста")
        return self._browser.find_elements(*locator)[item_number - 1].get_attribute(attribute)

    @allure.step("Получаем статус активности чекбокса")
    def _get_checkbox_status(self, locator):
        return self._browser.find_element(*locator).is_selected()

    @allure.step("Получаем значение CSS-свойства элемента по локатору")
    def _get_css(self, locator, css: str):
        self.wait_until_enabled(
            locator, "Элемент должен быть стабилен перед получением текста")
        return self._browser.find_element(*locator).value_of_css_property(css)

    @allure.step("Получаем координаты элемента по локатору")
    def _get_element_location(self, locator):
        return self._browser.find_element(*locator).location

    @allure.step("Получаем размеры элемента по локатору")
    def _get_element_size(self, locator):
        return self._browser.find_element(*locator).size

    @allure.step("Получаем список элементов по локатору")
    def _get_list_elements(self, locator):
        return self._browser.find_elements(*locator)

    @allure.step("Получаем значение свойства элемента по локатору")
    def _get_property(self, locator, property_element: str):
        element = self._browser.find_element(*locator)
        return element.get_property(property_element)

    @allure.step("Получаем текст элемента по локатору")
    def _get_text(self, locator):
        self.wait_until_present(
            locator, "Элемент должен быть стабилен перед получением текста")
        return self._browser.find_element(*locator).text

    @allure.step("Получаем текст элемента по локатору и номеру элемента")
    def _get_text_by_number(self, locator, item_number: int = 1):
        self.wait_until_enabled(
            locator, "Элемент должен быть стабилен перед получением текста")
        return self._browser.find_elements(*locator)[item_number - 1].text

    @allure.step("Получаем url страницы")
    def _get_url_page(self):
        return self._browser.current_url

    @allure.step("Возвращаемся на предыдущую страницу")
    def _go_to_previous_page(self):
        self._browser.back()
        time.sleep(0.5)

    @allure.step("Ввести текст в элемент по локатору")
    def _input(self, locator, text):
        self.wait_until_enabled(
            locator, "Элемент должен быть активен перед введением текста")
        self._browser.find_element(*locator).send_keys(text)

    @allure.step("Добавляем файл по локатору")
    def _input_file(self, locator, file):
        self._browser.find_element(*locator).send_keys(file)

    @allure.step("Вводим текст в модальное окно \"prompt\"")
    def _input_text_to_prompt(self, text):
        prompt = self._browser.switch_to.alert
        prompt.send_keys(text)
        prompt.accept()

    @allure.step("Получаем активность элемента по локатору")
    def _is_enabled(self, locator):
        element = self._is_present(locator, get_element=True)
        result = element and element.is_displayed() and element.is_enabled()
        allure.attach(str(result), "result")
        return result

    @abstractmethod
    def _is_opened(self, *args):
        ...

    @allure.step("Получаем существование элемента по локатору")
    def _is_present(self, locator, get_element=False):
        try:
            el = self._browser.find_element(*locator)
            result = el if get_element else True
        except NoSuchElementException:
            result = False

        allure.attach(str(result), "result")
        return result

    @allure.step("Получаем существование элемента внутри родителя по их локаторам")
    def _is_present_inside_parent(self, parent, locator, get_element=False):
        try:
            el = parent.find_element(*locator)
            result = el if get_element else True
        except NoSuchElementException:
            result = False

        allure.attach(str(result), "result")
        return result

    @allure.step("Получаем видимость элемента по локатору")
    def _is_visible(self, locator):
        element = self._is_present(locator, get_element=True)
        result = element and element.is_displayed()
        allure.attach(str(result), "result")
        return result

    @allure.step("Навести мышь на элемент по локатору")
    def _move_to(self, locator):
        ActionChains(self._browser).move_to_element(
            self._browser.find_element(*locator)).perform()

    @allure.step("Открываем новую вкладку")
    def _open_new_tab(self):
        self._browser.execute_script("window.open();")

    @allure.step("Нажимаем backspace")
    def _press_backspace(self):
        ActionChains(self._browser).send_keys(Keys.BACKSPACE).perform()

    @allure.step("Нажимаем Delete")
    def _press_delete(self):
        ActionChains(self._browser).send_keys(Keys.DELETE).perform()

    @allure.step("Нажимаем ввод")
    def _press_enter(self):
        ActionChains(self._browser).send_keys(Keys.ENTER).perform()

    @allure.step("Нажимаем Escape")
    def _press_escape(self):
        ActionChains(self._browser).send_keys(Keys.ESCAPE).perform()

    @allure.step("Эмулируем нажатие клавиши на клавиатуре")
    def _press_key(self, locator, button):
        el = self._browser.find_element(*locator)
        el.send_keys(button)

    @allure.step("Обновляем страницу")
    def _refresh_page(self):
        self._browser.refresh()

    @allure.step("Скроллим к элементу по локатору")
    def _scroll_to(self, locator, shift_x=0, shift_y=0):
        self.wait_until_present(
            locator, "Элемент должен присутствовать на странице перед скроллом на него")
        el_location = self._browser.find_element(*locator).location
        x = el_location["x"] + shift_x
        y = el_location["y"] + shift_y
        self._browser.execute_script(
            "window.scrollTo({}, {})".format(x, y))
        self.wait_until_visible(
            locator, "Элемент должен быть видим после скролла на него")

    @allure.step("Скроллим к концу страницы")
    def _scroll_to_page_down(self):
        ActionChains(self._browser).send_keys(Keys.PAGE_DOWN).perform()

    @allure.step("Скроллим к началу страницы")
    def _scroll_to_page_up(self):
        ActionChains(self._browser).send_keys(Keys.PAGE_UP).perform()

    @allure.step("Переключаем вкладку")
    def _switch_to_tab(self, tab):
        self._browser.switch_to.window(self._browser.window_handles[tab])
        time.sleep(0.5)

    def check_is_opened(self):
        if self._url:
            wait.until_ec(self._browser, EC.url_matches(
                self._url), " URL страницы не был открыт")
        self._is_opened()

    @allure.step("Ожидаем, что элемент содержит текст")
    def is_text_in_locator_is_present(self, locator, text):
        ec = EC.text_to_be_present_in_element(locator, text)
        wait.until_ec(self._browser, ec, f"Элемент не содержит текст: {text}")

    def open(self, need_check=True, url=None):
        current_url = self._url
        if url is not None:
            current_url = url

        with allure.step("Открываем страницу {}".format(current_url)):
            self._browser.get(current_url)
            if need_check:
                self._is_opened()

    @allure.step("Ожидаем, что чекбокс не выбран")
    def wait_checkbox_is_not_selected(self, locator, message="Чекбокс выбран", timeout=10):
        el = self._browser.find_element(*locator)
        ec = EC.element_to_be_selected(el)
        wait.until_not_ec(self._browser, ec, message, timeout)

    @allure.step("Ожидаем, что чекбокс выбран")
    def wait_checkbox_is_selected(self, locator, message="Чекбокс не выбран", timeout=10):
        el = self._browser.find_element(*locator)
        ec = EC.element_to_be_selected(el)
        wait.until_ec(self._browser, ec, message, timeout)

    @allure.step("Ожидаем, что загрузка файла началась и завершена")
    def wait_for_start_and_finish_file_download(self):
        om.check_file_start_to_download()
        om.wait_until_file_downloading()

    @allure.step("Ждем, пока модальное окно alert пропадет")
    def wait_until_alert_not_present(self, message):
        ec = EC.alert_is_present()
        wait.until_not_ec(self._browser, ec, message)

    @allure.step("Ожидаем, что текущий URL содержит подстроку")
    def wait_until_current_url_contains_parameter(self, url, message, timeout=10):
        ec = EC.url_contains(url)
        wait.until_ec(self._browser, ec,
                      f"{message}. В URL не найдена подстрока: {url}", timeout)

    @allure.step("Ждём, пока элемент по локатору станет не активен")
    def wait_until_disabled(self, locator, message, timeout=10):
        ec = EC.element_to_be_clickable(locator)
        wait.until_not_ec(self._browser, ec, "{}: {}".format(
            ",".join(locator), message), timeout=timeout)

    @allure.step("Ждём, пока элемент по локатору не пропадет со страницы")
    def wait_until_disappeared(self, locator, message, timeout=10):
        ec = EC.presence_of_element_located(locator)
        wait.until_not_ec(self._browser, ec, "{}: {}".format(
            ",".join(locator), message), timeout)

    @allure.step("Ждём появления элемента с перезагрузкой страницы")
    def wait_until_element_present_with_refresh_page(self, locator, message, timeout=10):
        end_time = time.time() + timeout
        count = 1
        while True:
            with allure.step(f"Ждем 3 секунды. Получаем элемент, попытка {count}"):
                if self._is_present(locator):
                    return False
            self._refresh_page()
            time.sleep(3)
            count += 1
            if time.time() > end_time:
                break
        raise TimeoutException(message)

    @allure.step("Ждём, пока текст элемента изменится")
    def wait_until_element_text_changed(self, locator, text, timeout=10):
        end_time = time.time() + timeout
        count = 1
        while True:
            with allure.step(f"Ждем 2 секунды. Получаем текст элемента, попытка {count}"):
                text_element = self._get_text(locator)
                if text_element == text:
                    return True
            time.sleep(2)
            count += 1
            if time.time() > end_time:
                break
        print(f"Текст элемента '{text_element}', должен быть равен '{text}'")
        raise TimeoutException("Не изменился текст элемента")

    @allure.step("Ждём, пока текст элемента изменится")
    def wait_until_element_text_changed_with_refresh_page(self, locator, text, timeout=10):
        end_time = time.time() + timeout
        count = 1
        while True:
            with allure.step("Ждем 2 секунды. Получаем текст элемента, попытка {count}"):
                text_element = self._get_text(locator)
                if text_element == text:
                    return False
            self._refresh_page()
            time.sleep(3)
            count += 1
            if time.time() > end_time:
                break
        print(f"Текст элемента '{text_element}', должен быть равен '{text}'")
        raise TimeoutException("Не изменился текст элемента")

    @allure.step("Ждём, пока текст элемента не перестанет быть равным текущему")
    def wait_until_element_by_number_text_is_no_longer_equal_to_current(self, locator, item, text, timeout=10):
        end_time = time.time() + timeout
        count = 1
        while True:
            with allure.step("Ждем 1 секунду. Получаем текст элемента, попытка {count}"):
                text_element = self._get_text_by_number(locator, item)
                if text_element != text:
                    return False
            time.sleep(1)
            count += 1
            if time.time() > end_time:
                break
        print(
            f"Текст элемента '{text_element}', не должен быть равен '{text}'")
        raise TimeoutException("Не изменился текст элемента")

    @allure.step("Ждём, пока текст элемента не перестанет быть равным текущему")
    def wait_until_element_text_is_no_longer_equal_to_current(self, locator, text, timeout=10):
        end_time = time.time() + timeout
        count = 1
        while True:
            with allure.step("Ждем 1 секунду. Получаем текст элемента, попытка {count}"):
                text_element = self._get_text(locator)
                if text_element != text:
                    return False
            time.sleep(1)
            count += 1
            if time.time() > end_time:
                break
        print(
            f"Текст элемента '{text_element}', не должен быть равен '{text}'")
        raise TimeoutException("Не изменился текст элемента")

    @allure.step("Ждём, пока элемент по локатору не станет активен")
    def wait_until_enabled(self, locator, message, timeout=10, poll=0.5):
        ec = EC.element_to_be_clickable(locator)
        wait.until_ec(self._browser, ec, "{}: {}".format(
            ",".join(locator), message), timeout=timeout, poll=poll)

    @allure.step("Ждём, пока элемент по локатору не станет невидим")
    def wait_until_invisible(self, locator, message, timeout=10, poll=0.5):
        ec = EC.invisibility_of_element_located(locator)
        wait.until_ec(self._browser, ec, "{}: {}".format(
            ",".join(locator), message), timeout=timeout, poll=poll)

    @allure.step("Ждём, пока элемент по локатору не появится на странице")
    def wait_until_present(self, locator, message, timeout=10, poll=0.5):
        ec = EC.presence_of_element_located(locator)
        wait.until_ec(self._browser, ec, "{}: {}".format(
            ",".join(locator), message), timeout=timeout, poll=poll)

    @allure.step("Ждём, пока элемент по локатору не появится внутри родителя")
    def wait_until_present_inside_parent(self, parent, locator, message, timeout=10, poll=0.5):
        ec = EC.presence_of_element_located(locator)
        wait.until_ec(parent, ec, "{}: {}".format(
            ",".join(locator), message), timeout=timeout, poll=poll)

    @allure.step("Ждём, пока элемент по локатору не станет видим")
    def wait_until_visible(self, locator, message, poll=0.5):
        ec = EC.visibility_of_element_located(locator)
        wait.until_ec(self._browser, ec, "{}: {}".format(
            ",".join(locator), message), poll=poll)


class BaseLocators(Enum):
    @classmethod
    @allure.step("Добавляем к локатору дочерний локатор")
    def add_child(cls, parent: tuple, locator: tuple, direct_descendant=False):
        parent_loc_list = list(parent)
        item_loc_list = list(locator)
        if direct_descendant:
            parent_loc_list[1] = "{} > {}".format(
                parent_loc_list[1], item_loc_list[1])
        else:
            parent_loc_list[1] = "{} {}".format(
                parent_loc_list[1], item_loc_list[1])
        return tuple(parent_loc_list)

    @classmethod
    @allure.step("Добавляем текст в конец локатора")
    def append_text_to_locator(cls, locator: tuple, text: int or str):
        item_loc_list = list(locator)
        item_loc_list[1] = f"{item_loc_list[1]}{text}"
        return tuple(item_loc_list)

    @classmethod
    @allure.step("Форматируем шаблон локатора параметрами")
    def format_locator(cls, locator_tmpl: tuple, *placeholders):
        item_loc_list = list(locator_tmpl)
        item_loc_list[1] = item_loc_list[1].format(*placeholders)
        return tuple(item_loc_list)

    @classmethod
    @allure.step("Получаем локатор с :nth-child")
    def get_nth_child(cls, locator: tuple, item_num: int):
        item_loc_list = list(locator)
        item_loc_list[1] = item_loc_list[1] + f":nth-child({item_num})"
        return tuple(item_loc_list)

    @classmethod
    @allure.step("Получаем локатор с :nth-of-type")
    def get_nth_of_type(cls, locator: tuple, item_num: int):
        item_loc_list = list(locator)
        item_loc_list[1] = item_loc_list[1] + f":nth-of-type({item_num})"
        return tuple(item_loc_list)

    @classmethod
    @allure.step("Получаем локатор с :nth-last-child")
    def get_nth_last_child(cls, locator: tuple, item_num: int):
        item_loc_list = list(locator)
        item_loc_list[1] = item_loc_list[1] + f":nth-last-child({item_num})"
        return tuple(item_loc_list)
