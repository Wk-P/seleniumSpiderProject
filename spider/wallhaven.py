import requests
import selenium_project.ChromeTools as Tools
from selenium_project.ChromeTools import find_element_by_xpath as get_element_by_xpath


def Spider(url):
    driver = Tools.WallHavenChromeDriver("https://wallhaven.cc/latest?page=2", ["--headless"])
    max_size = 50
    # 起始爬取
    driver.check_element(Tools.By.XPATH, '//*[@id="thumbs"]/section')
    sections = driver.find_elements_by_xpath('//*[@id="thumbs"]/section')
    index = 1
    pages = 2
    gotten_size = 0
    ''' 假设需要爬6个section
        先获取到6个section
        再爬
    '''
    while gotten_size <= 2:
        for section in sections:
            gotten_size += 1
            img_lis = Tools.find_elements_by_xpath(section, 'ul/li')
            for img in img_lis:
                img_link = get_element_by_xpath(img, 'figure/a').get_attribute('href')

                # 切换至当前界面
                driver.open_new_window_label(img_link)

                # 定位下载连接, 下载并保存
                if driver.check_element(Tools.By.XPATH, '//*[@id="wallpaper"]'):
                    download_url = driver.find_element_by_xpath('//*[@id="wallpaper"]').get_attribute('src')
                    img = requests.get(download_url).content
                    filename = "../img/wallimg/Lastest" + str(index) + '.png'
                    with open(filename, 'wb') as imgFile:
                        imgFile.write(img)

                print("已下载 %s 张图片" % index)

                # 单页图片下标
                index += 1

                # 关闭当前子标签，回到父标签
                driver.close()
                driver.switch_window_to(driver.get_window_handles()[0])
            # 网页section 滚动计数
            pages -= 1

        # 滚动条下拉
        while True:
            driver.move_scroll()
            sections = driver.find_elements_by_xpath('//*[@id="thumbs"]/section')
            if gotten_size == len(sections):
                continue
            else:
                break

        if len(sections) > 1:
            for m in range(gotten_size):
                sections.remove(sections[0])
        else:
            pass

    print("下载完毕!")


if __name__ == "__main__":
    Spider("https://wallhaven.cc/latest?page=2")
