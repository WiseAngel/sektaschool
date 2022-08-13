import allure
from selenium.common.exceptions import TimeoutException

import utils.wait_utils as wait


def contains(substring, string, message, error_message=None):
    def method():
        with allure.step(
                "Проверить содержание подстроки в строке: substring = {}, string = {}".format(substring, string)):
            assert substring in string, error_message if error_message else message

    step(method, message)


def equals(actual, expected, message, error_message=None):
    def method():
        with allure.step("Проверить равенство объектов: actual = {}, expected = {}".format(actual, expected)):
            assert actual == expected, error_message if error_message else message

    step(method, message)


def false(condition, message, error_message=None):
    def method():
        with allure.step("Проверить провал условия: {}".format(get_condition_name(condition))):
            assert not condition(), error_message if error_message else message

    step(method, message)


def get_condition_name(condition):
    return "{}.{}".format(type(condition.__self__).__name__, condition.__name__)


def greater_than_or_equal_to(actual, expected, message, error_message=None):
    def method():
        with allure.step(
                "Проверить, что один объект больше другого или равен ему: first_value = {}, second_value = {}".format(
                    actual, expected)):
            assert actual >= expected, error_message if error_message else message

    step(method, message)


def in_range(actual, expected_less, expected_more, message, error_message=None):
    def method():
        with allure.step(
                f"Проверить, что значение объекта попадает в диапазон: {expected_less} <= {actual} <= {expected_more}"):
            assert expected_less <= actual <= expected_more, error_message if error_message else message

    step(method, message)


def less_than(actual, expected, message, error_message=None):
    def method():
        with allure.step(
                "Проверить, что один объект больше другого: first_value = {}, second_value = {}".format(actual,
                                                                                                        expected)):
            assert actual < expected, error_message if error_message else message

    step(method, message)


def not_contains(substring, string, message, error_message=None):
    def method():
        with allure.step(
                "Проверить отсутствие подстроки в строке: substring = {}, string = {}".format(substring, string)):
            assert substring not in string, error_message if error_message else message

    step(method, message)


def not_equals(actual, expected, message, error_message=None):
    def method():
        with allure.step(
                "Проверить неравенство объектов: first_value = {}, second_value = {}".format(actual, expected)):
            assert actual != expected, error_message if error_message else message

    step(method, message)


def step(method, message):
    with allure.step(f"Проверяем, что {message}"):
        method()


def true(condition, message, error_message=None):
    def method():
        with allure.step("Проверить выполнение условия: {}".format(get_condition_name(condition))):
            assert condition(), error_message if error_message else message

    step(method, message)


def wait_false(condition, message, error_message=None):
    def method():
        with allure.step("Ждать провала условия: {}".format(get_condition_name(condition))):
            try:
                wait.until_not(condition, error_message if error_message else message)
            except TimeoutException:
                raise AssertionError(error_message if error_message else message)

    step(method, message)


def wait_true(condition, message, error_message=None, timeout=10):
    def method():
        with allure.step("Ждать выполнения условия: {}".format(get_condition_name(condition))):
            try:
                wait.until(condition, error_message if error_message else message, timeout=timeout)
            except TimeoutException:
                raise AssertionError(error_message if error_message else message)

    step(method, message)
