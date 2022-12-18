import json
import selenium_project.ChromeTools as Tools
from selenium_project.ChromeTools import find_element_by_xpath as get_element_by_xpath
import os


def Spider(_url):
    driver = Tools.BLChromeDriver(_url)
    max_size = 100
    title = None
    if driver.check_element(Tools.By.XPATH, '/html/body/iframe'):
        title = driver.find_element_by_xpath('//*[@id="viewbox_report"]/h1').text
    filename = r'../data_files/' + title + '.jsonl'
    gotten_size = 0
    with open(filename, 'w', encoding='utf-8') as f:
        while max_size > 0:
            if driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]'):
                user_comments = driver.find_elements_by_xpath('//*[@id="comment"]/div/div/div/div[2]/div[2]/div')
                user_comments.remove(user_comments[-1])
                # comment_block 评论主题框架
                for comment_block in user_comments:
                    if driver.check_element(Tools.By.XPATH, '//*[@id="comment"]/div/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]/span/span'):
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
                        max_size -= 1
                        json.dump(dict({'name': name, 'comment': comment}), f, ensure_ascii=False)
                        f.write('\n')
                    else:
                        print("爬取完成!")
                        break

        # 滚动条更新评论
        while len(user_comments) == gotten_size:
            driver.move_scroll()
            user_comments = driver.find_elements_by_xpath('//*[@id="comment"]/div/div/div/div[2]/div[2]/div')
            user_comments.remove(user_comments[-1])

        if len(user_comments):
            del user_comments[0:gotten_size]
    driver.close()
    return filename


if __name__ == "__main__":
    url = 'https://www.bilibili.com/video/BV1CG4y157Nx/?spm_id_from=333.1007.tianma.1-1-1.click&vd_source=fa1028ee348b8a952050f54821408b19'
    filename = Spider(url)

