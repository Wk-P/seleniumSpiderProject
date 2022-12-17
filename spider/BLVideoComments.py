import json
import selenium_project.ChromeTools as Tools
from selenium_project.ChromeTools import find_element_by_xpath as get_element_by_xpath


def Spider(url):
    driver = Tools.BLChromeDriver(url)
    max_size = 10
    title = None
    if driver.check_element(Tools.By.XPATH, '/html/body/iframe'):
        title = driver.find_element_by_xpath('//*[@id="viewbox_report"]/h1').text
    filename = '../file/' + title + '.jsonl'
    with open(filename, 'w', encoding='utf-8') as f:
        if driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div'):
            user_comments = driver.find_elements_by_xpath('//*[@id="comment"]/div/div/div/div[2]/div[2]/div')
            user_comments.remove(user_comments[-1])
            for comment_block in user_comments:
                print(comment_block)
                # 爬取写入
                if driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]') \
                        and driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[3]/span'):
                    name = get_element_by_xpath(comment_block, 'div[2]/div[2]/div[2]/div').text
                    comment = get_element_by_xpath(comment_block, 'div[2]/div[2]/div[3]/span/span').text
                else:
                    print("爬取完成!")
                    break
                json.dump(dict({'name': name, 'comment': comment}), f, ensure_ascii=False)
                f.write('\n')
    # driver.close()


def main(url):
    Spider(url)


if __name__ == "__main__":
    Spider('https://www.bilibili.com/video/BV1ed4y1v71q/?spm_id_from=333.999.0.0&vd_source=fa1028ee348b8a952050f54821408b19')

