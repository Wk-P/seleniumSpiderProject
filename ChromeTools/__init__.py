from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import selenium.webdriver.support.expected_conditions as EC
import json


# json 转 字符串
def jsonToString(datas):
    name_list = list(datas)
    value_list = list(datas.values())
    for (name, value) in zip(name_list, value_list):
        yield name + '=' + value


def find_element_by_xpath(parent, xpath):
    return parent.find_element(by=By.XPATH, value=xpath)


def find_elements_by_xpath(parent, xpath):
    return parent.find_elements(by=By.XPATH, value=xpath)


def switch_window_to(driver, window):
    driver.switch_to.window(window)


def move_scroll(driver, coefficient=0.7, move_height=None):
    if move_height is None:
        move_height = driver.execute_script('return window.innerHeight * ' + str(coefficient) + ';')
    js = 'window.scrollBy({top: ' + str(move_height) + '})'
    driver.execute_script(js)


class ChromeDriver:
    driver = None
    service = None
    options = webdriver.ChromeOptions()
    options_args = list()
    start_url = None
    cookies = None
    another_args = list()

    def __init__(self, url, cookies=None, options_args=None, another_args=None):
        self.start_url = url
        self.service = Service(ChromeDriverManager().install())

        if options_args is not None:
            self.options_args = options_args
            for arg in self.options_args:
                self.options.add_argument(arg)

        if another_args is not None:
            self.another_args = another_args
            for arg in self.another_args:
                self.options.add_argument(arg)

        self.cookies = cookies
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def run(self):
        self.driver.get(self.start_url)
        if self.cookies is not None:
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def find_element_by_xpath(self, xpath):
        return self.driver.find_element(by=By.XPATH, value=xpath)

    def find_elements_by_xpath(self, xpath):
        return self.driver.find_elements(by=By.XPATH, value=xpath)

    def check_element(self, pattern, value):
        try:
            WebDriverWait(self.driver, 20, 0.01).until(EC.presence_of_element_located((pattern, value)))
            return True
        except StaleElementReferenceException:
            return False

    def close(self):
        self.driver.quit()

    def move_scroll(self, move_height=None):
        if move_height is None:
            move_height = self.driver.execute_script('return window.innerHeight * 0.7;')
        js = 'window.scrollBy({top: ' + str(move_height) + '})'
        self.driver.execute_script(js)


class BLChromeDriver:
    service = None
    options = webdriver.ChromeOptions()
    options_args = list()
    another_args = ["--start-maximized"]
    start_url = None
    cookies = None
    driver = None

    def __init__(self, url):
        with open("../file/options_arguments.json", "r") as json_file:
            datas = json.load(json_file)
            for data in jsonToString(datas):
                self.options_args.append(data)
        self.service = Service(ChromeDriverManager().install())
        for arg in self.options_args:
            self.options.add_argument(arg)

        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.start_url = url
        self.driver.get(self.start_url)

        # auto login
        with open("../file/cookies.json", 'r') as cookies_file:
            self.cookies = json.load(cookies_file)
            for cookie in self.cookies:
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    def find_element_by_xpath(self, xpath):
        return self.driver.find_element(by=By.XPATH, value=xpath)

    def find_elements_by_xpath(self, xpath):
        return self.driver.find_elements(by=By.XPATH, value=xpath)

    def check_element(self, pattern, value):
        try:
            WebDriverWait(self.driver, 20, 0.01).until(EC.presence_of_element_located((pattern, value)))
            return True
        except StaleElementReferenceException:
            return False

    def close(self):
        self.driver.quit()

    def move_scroll(self, move_height=None):
        if move_height is None:
            move_height = self.driver.execute_script('return window.innerHeight * 0.7;')
        js = 'window.scrollBy({top: ' + str(move_height) + '})'
        self.driver.execute_script(js)


class WallHavenChromeDriver:
    service = None
    options = webdriver.ChromeOptions()
    options_args = list()
    another_args = []
    start_url = None
    cookies = None
    driver = None

    def __init__(self, url, args):
        for arg in args:
            self.another_args.append(arg)
        with open("../file/options_arguments.json", "r") as json_file:
            datas = json.load(json_file)
            for data in jsonToString(datas):
                self.options_args.append(data)
        for arg in self.another_args:
            self.options.add_argument(arg)
        self.service = Service(ChromeDriverManager().install())
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.start_url = url
        self.driver.get(self.start_url)

    def find_element_by_xpath(self, xpath):
        return self.driver.find_element(by=By.XPATH, value=xpath)

    def find_elements_by_xpath(self, xpath):
        return self.driver.find_elements(by=By.XPATH, value=xpath)

    def check_element(self, pattern, value):
        try:
            WebDriverWait(self.driver, 20, 0.01).until(EC.presence_of_element_located((pattern, value)))
            return True
        except StaleElementReferenceException:
            return False

    # 退出浏览器
    def quit(self):
        self.driver.quit()

    # 关闭当前标签页
    def close(self):
        self.driver.close()

    def get(self, url):
        self.driver.get(url)

    def open_new_window_label(self, url):
        js = 'window.open("' + url + '")'
        self.driver.execute_script(js)
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def switch_window_to(self, window):
        self.driver.switch_to.window(window)

    def get_window_handles(self):
        return self.driver.window_handles

    def move_scroll(self, move_height=None):
        if move_height is None:
            move_height = self.driver.execute_script('return window.innerHeight * 0.7;')
        js = 'window.scrollBy({top: ' + str(move_height) + '})'
        self.driver.execute_script(js)
