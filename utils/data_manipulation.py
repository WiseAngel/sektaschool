from datetime import datetime
from random import randint, sample, choice
import string

import allure


@allure.step("Конвертируем время из ISO-формата в JS Locale String")
def convert_date_from_iso_to_locale_string(browser, iso_time, locale="ru", time_options=None):
    if time_options is None:
        time_options = {
            "day": "numeric",
            "month": "long",
            "year": "numeric"
        }

    res_data = browser.execute_script(
        f"var close_date = new Date(\"{iso_time}\"); return close_date.toLocaleString(\"{locale}\", {time_options});")

    return res_data


@allure.step("Получаем новый цвет")
def get_new_color():
    return "rgba({}, {}, {}, 1)".format(*sample(range(0, 255), 3))


@allure.step("Получаем новое значение поля ввода")
def get_new_score(current_score, min_score=1, max_score=9):
    with allure.step(f"Получаем новое значение поля ввода от {min_score} до {max_score}"):
        count = 1
        new_score = get_random_score(min_score, max_score)
        while new_score == current_score and count <= 10:
            with allure.step(f"Генерируем число отличное от текущего, попытка {count}"):
                count += 1
                new_score = get_random_score()
        return new_score


@allure.step("Получаем случайное число")
def get_random_score(min_score=1, max_score=9):
    with allure.step(f"Получаем случайное число от {min_score} до {max_score}"):
        return str(randint(min_score, max_score))


@allure.step("Получаем случайную строку")
def get_random_string(number=10):
    with allure.step(f"Получаем случайную строку длиной {number} символов"):
        letters = string.ascii_lowercase
        return "".join(choice(letters) for _ in range(number))


@allure.step("Генерируем уникальное имя")
def get_uniq_name(name):
    return f"{name} {str(datetime.now())}"
