from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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


class BLChromeDriver:
    BL_service = None
    BL_options = webdriver.ChromeOptions()
    options_arguments = []
    another_arguments = []
    start_url = "https://space.bilibili.com/44629592/bangumi"
    cookies = None
    chrome_driver = None

    def __init__(self):
        with open("../file/options_arguments.json", "r") as json_file:
            datas = json.load(json_file)
            for data in jsonToString(datas):
                self.options_arguments.append(data)
        for argument in self.another_arguments:
            self.options_arguments.append(argument)

    def init_chrome_driver(self):
        self.BL_service = Service(ChromeDriverManager().install())
        for argument in self.options_arguments:
            self.BL_options.add_argument(argument)
        self.chrome_driver = webdriver.Chrome(service=self.BL_service, options=self.BL_options)
        self.chrome_driver.get(self.start_url)

    def login_BL(self):
        with open("../file/cookies.json", 'r') as cookies_file:
            self.cookies = json.load(cookies_file)
            for cookie in self.cookies:
                self.chrome_driver.add_cookie(cookie)
        self.chrome_driver.refresh()

    def find_element_by_xpath(self, xpath):
        return self.chrome_driver.find_element(by=By.XPATH, value=xpath)

    def find_elements_by_xpath(self, xpath):
        return self.chrome_driver.find_elements(by=By.XPATH, value=xpath)

    def check_element(self, pattern, value):
        flag = None
        try:
            WebDriverWait(self.driver, 20, 0.01).until(EC.presence_of_element_located((pattern, value)))
        except NoSuchElementException:
            flag = False
        else:
            flag = True
        finally:
            return flag

    def close(self):
        self.chrome_driver.quit()


if "__main__" == __name__:
    # 打开 登录我的追番
    my_driver = BLChromeDriver()
    my_driver.init_chrome_driver()
    my_driver.login_BL()

    items_info = list()
    pages_options = list()
    while True:
        check_item_xpath = '//*[@id="page-bangumi"]/div/div[2]/div/div/ul/li[1]/a[2]/h4'
        item_xpath = '//*[@id="page-bangumi"]/div/div[2]/div/div/ul/li'
        if my_driver.check_element(pattern=By.XPATH, value=check_item_xpath):
            items = my_driver.find_elements_by_xpath(item_xpath)
            items.remove(items[-1])
            for item in items:
                info = dict()
                info['title'] = item.find_element(by=By.XPATH, value='a[2]/h4').text
                info['watche-state'] = item.find_element(by=By.XPATH, value='a[2]/div[3]/span[1]').text
                info['publish-state'] = item.find_element(by=By.XPATH, value='a[2]/div[3]/span[2]').text
                items_info.append(info)
        else:
            print("No Element!")

        check_page_xpath = '//*[@id="page-bangumi"]/div/div[2]/div/div/div/a[1]'
        page_xpath = '//*[@id="page-bangumi"]/div/div[2]/div/div/div/a'
        if my_driver.check_element(pattern=By.XPATH, value=check_page_xpath):
            pages_options = my_driver.find_elements_by_xpath(page_xpath)
            next_page_option = pages_options[-1]
            if next_page_option.text == "下一页":
                next_page_option.click()
            else:
                print("爬取完毕")
                break
        else:
            print("No Element!")

    json_filename = "../data_files/我的追番.jsonl"
    with open(json_filename, 'w', encoding='utf-8') as f:
        for item_info in items_info:
            json.dump(item_info, f, ensure_ascii=False)
            f.write('\n')
    my_driver.close()