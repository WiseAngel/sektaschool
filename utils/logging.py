import json
import os
from pathlib import Path


class Logs:
    @classmethod
    def create_dir(cls, path, file_name):
        Path(path).mkdir(parents=True, exist_ok=True)
        return os.path.join(path, file_name)

    @classmethod
    def get_browser_logs(cls, browser, path, file_name):
        path = os.path.join(path, "browser_logs")
        path_fo_file = cls.create_dir(path, file_name)
        log = browser.get_log("browser")
        if log:
            cls.write_file(path_fo_file, log)

    @classmethod
    def get_network_logs(cls, browser, path, file_name):
        path_fo_file = os.path.join(path, file_name)
        log = browser.execute_script("return window.performance.getEntries();")
        cls.write_file(path_fo_file, log)

    @classmethod
    def get_performance_logs(cls, browser, path, file_name):
        path = os.path.join(path, "performance_logs")
        path_fo_file = cls.create_dir(path, file_name)
        log = browser.get_log("performance")
        cls.write_file(path_fo_file, log)

    @classmethod
    def write_file(cls, path_fo_file, log):
        with open(path_fo_file, "w") as f:
            json.dump(log, f)
