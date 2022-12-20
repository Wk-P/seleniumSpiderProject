import json
import time

import selenium_project.ChromeTools as Tools
from selenium_project.ChromeTools import find_element_by_xpath as get_element_by_xpath


def Spider(_url=None):
    if _url is None or _url == '':
        print("Invalid url!")
        exit()

    driver = Tools.BLChromeDriver(_url)
    max_size = 500

    # 标题
    driver.check_element(Tools.By.XPATH, '//*[@id="viewbox_report"]/h1')
    title = driver.find_element_by_xpath('//*[@id="viewbox_report"]/h1').text

    filename = r'../data_files/' + title + '.jsonl'
    gotten_size = 0

    # 评论区
    driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]/div[2]')
    user_comments = driver.find_elements_by_xpath('//*[@id="comment"]/div/div/div/div[2]/div[2]/div')

    with open(filename, 'w', encoding='utf-8') as f:

        while gotten_size <= max_size:
            user_comments.remove(user_comments[-1])
            # comment_block 评论主题框架
            for comment_block in user_comments:
                driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]/div[2]/div')
                # 笔记和普通评论的共同父结点
                extract = get_element_by_xpath(comment_block, 'div[2]/div[2]')
                if extract.find_element(by=Tools.By.XPATH, value='div[3]/div[1]').get_attribute('class') == 'note-content':
                    # 笔记
                    name = get_element_by_xpath(extract, 'div[2]/div').text
                    comment = get_element_by_xpath(extract, 'div[3]/div[1]/div[1]/span').text
                else:
                    # 普通评论
                    name = get_element_by_xpath(extract, 'div[2]/div').text
                    comment = get_element_by_xpath(extract, 'div[3]/span').text

                # 写入文件
                gotten_size += 1
                json.dump(dict({'name': name, 'comment': comment}), f, ensure_ascii=False)
                f.write('\n')

                if gotten_size > max_size:
                    break

            # 下拉滚动条值底部
            driver.move_scroll()
            # time.sleep()
            driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]/div[2]/div/div[1]')
            time.sleep(2.3)
            user_comments = driver.find_elements_by_xpath('//*[@id="comment"]/div/div/div/div[2]/div[2]/div')

            if user_comments[-1].get_attribute('class') == 'reply-end':
                print("爬取完成!")
                break

            if gotten_size > max_size:
                print("爬取完成!")
                break

            if len(user_comments) > gotten_size:
                del user_comments[0:gotten_size]

        print("爬取结束!")
        driver.close()


if __name__ == "__main__":
    url = ''
    Spider(url)

