from DrissionPage import ChromiumPage
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import re
import pymysql
# 创建单个page对象
page = ChromiumPage()
#————————————————————————————————————————————————————————————————————————————————————————————————————————
# 第三版，增加URL过滤
def fetch_urls(base_url):
    driver = webdriver.Chrome()  # 使用适当的驱动程序
    driver.get(base_url)  # 打开网页
    urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")  # 获取页面高度

    url_pattern = re.compile(r'https://www\.zhihu\.com/question/\d+') # 筛选url，用正则表达式

    while True:
        list_items = driver.find_elements(By.CLASS_NAME, "List-item.TopicFeedItem")
        for item in list_items:
            try:
                url_element = item.find_element(By.CSS_SELECTOR, "[itemprop='url']")
                url = url_element.get_attribute("content")
                if url and url_pattern.match(url):  # 过滤符合特定模式的URL
                    urls.add(url)
            except Exception as e:
                continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待页面加载
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # 如果页面高度没有变化，说明已经滚动到底部
            break
        last_height = new_height

    driver.quit()
    return list(urls)
#——————————————————————————————————————————————————————————————————————————————————————————————————————————
def scrape_page_data(url):
    try:
        page.get(url)
        page_data = {}
        
        title_ele = page.ele("tag:h1@class=QuestionHeader-title")
        page_data['question_title'] = title_ele.text if title_ele else ""
        
        text_ele = page.ele("tag:span@itemprop=text")
        page_data['question_text'] = text_ele.text if text_ele else ""

        topic_links = page.eles("tag:a@class=TopicLink")
        topics = [{'text': l.ele("tag:div@class=css-1gomreu").text, 'url': l.attr('href')} for l in topic_links] if topic_links else []
        page_data['topics'] = topics

        followers_ele = page.ele("tag:strong@class=NumberBoard-itemValue")
        page_data['followers']=followers_ele.text if followers_ele else ""

        views_ele = page.ele("tag:strong@class=NumberBoard-itemValue")
        page_data['views'] = views_ele.text if views_ele else ""

        number_board_items = page.eles("tag:div@class=NumberBoard-itemInner")
        if number_board_items:
            for item in number_board_items:
                # item_name = item.ele("tag:div@class=NumberBoard-itemName").text
                item_value = item.ele("tag:strong@class=NumberBoard-itemValue").text
                page_data['item_value'] = item_value

        good_question_action = page.ele("tag:div@class=GoodQuestionAction")
        page_data['likes'] = good_question_action.ele("tag:button").text if good_question_action else ""

        print(f"抓取数据 {url} 完成")
        return page_data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
#——————————————————————————————————————————————————————————————————————————————————————————————————————————
def save_to_csv(data, filename='健身增肌.csv'):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['url', 'question_title', 'question_text', 'topics', 'followers', 'views', 'likes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for url, info in data.items():
            row = {
                'url': url,
                'question_title': info.get('question_title', ''),
                'question_text': info.get('question_text', ''),
                'topics': ', '.join([t['text'] for t in info.get('topics', [])]),
                'followers': str(info.get('item_value', ''))[0],
                'views': str(info.get('item_value', ''))[1],
                'likes': info.get('likes', '')
            }
            writer.writerow(row)
#——————————————————————————————————————————————————————————————————————————————————————————————————————————
def main():
    base_url = "https://www.zhihu.com/topic/19941114/top-answers"
    all_urls = fetch_urls(base_url)
    data = {}
    for url in all_urls:
        page_data = scrape_page_data(url)
        if page_data:
            data[url] = page_data

    save_to_csv(data)

if __name__ == "__main__":
    try:
        results = main()
    finally:
        # 程序结束前关闭浏览器
        page.close()