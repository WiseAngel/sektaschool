import glob
import os
import shutil
import tempfile
import time

import allure
from selenium.common.exceptions import TimeoutException

import core.context as ctx

default_timeout = 60


@allure.step("Добавляем новую папку")
def add_new_directory(name_directory):
    path = os.path.join(tempfile.gettempdir(), name_directory)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


@allure.step("Получаем наличие файла в директории")
def check_file_in_dir_present(file_name, timeout=10):
    count = 1
    end_time = time.time() + timeout
    name_directory = ctx.DOWNLOAD_FOLDER
    path = os.path.join(tempfile.gettempdir(), name_directory)

    while True:
        with allure.step(f"Ждем 1 секунду. Проверяем наличие файла в директории, попытка {count}"):
            if file_name in os.listdir(path):
                return True
            if time.time() > end_time:
                return False
            else:
                count += 1
                time.sleep(1)


@allure.step("Проверяем, что началась загрузка файла")
def check_file_start_to_download():
    path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
    end_time = time.time() + 5
    while True:
        if len(os.listdir(path)):
            return False
        time.sleep(1)
        if time.time() > end_time:
            break
    raise TimeoutException("Не началась загрузка файла")


@allure.step("Удаляем папку")
def delete_directory(path_directory):
    os.rmdir(path_directory)


@allure.step("Удаляем файл")
def delete_file(file_path):
    os.unlink(file_path)


@allure.step("Удаляем содержимое папки")
def delete_files_of_directory():
    path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Ошибка удаления %s. Причина: %s" % (file_path, e))


@allure.step("Получаем количество файлов в папке")
def get_amount_files_of_directory():
    path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
    return len(os.listdir(path))


@allure.step("Получаем размер файла")
def get_size_file(file_name):
    return os.path.getsize(os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER, file_name))


@allure.step("Ожидаем загрузки файла")
def wait_until_file_downloading():
    end_time = time.time() + default_timeout
    path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
    while True:
        if not glob.glob(path + "\\*.crdownload"):
            return False
        time.sleep(2)
        if time.time() > end_time:
            break
    raise TimeoutException("Не загрузился файл")
