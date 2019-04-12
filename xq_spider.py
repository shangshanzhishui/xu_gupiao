from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import csv
from urllib import request
import time

def handle_name(items):
    """处理名字"""
    time.sleep(5)
    href = items[1].select("a")[0]["href"]
    href = "https://xueqiu.com" + href


    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = request.Request(url=href, headers=headers)
    html = request.urlopen(req)

    soup = BeautifulSoup(html, "lxml")
    s = soup.select(".stock-name")[0].get_text()
    # print(s)

    return s


num = 0 #初始化股票数量
browser = webdriver.Firefox()
browser.get("https://xueqiu.com/hq#exchange=US&firstName=3&secondName=3_0&order=desc&orderby=percent")
whait = WebDriverWait(browser,40)#等待时间
#滚动页面
browser.execute_script("""var h = document.body.scrollHeight, 
            k = 0;
        var timer = setInterval(function() {
            k += 150;
            console.log(k);
            if (k > h) clearInterval(timer);
            window.scrollTo(0,k);
        }, 500);""")
#等待直到加载出制定标签
whait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".next"))
    )

f = open("r.csv","w")
field_name = ["股票代码","股票名称","当前价格","涨跌额","市盈率(TTM)","市值"]
w = csv.DictWriter(f,fieldnames=field_name)
w.writeheader()
for i in range(1000):#

    # whait.until(
    #         EC.presence_of_element_located(
    #             (By.CSS_SELECTOR, ""))
    #     )
    html = browser.page_source
    soup = BeautifulSoup(html,"lxml")
    l = soup.select("#stockList > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr")

    for items in l:
        num += 1
        items = items.select("td")
        # print(items)
        xq_news = {"股票代码":items[0].select("a")[0].get_text(),
                    "股票名称":handle_name(items),
                   "当前价格":items[2].select("span")[0].get_text(),
                   "涨跌额":items[3].get_text(),
                   "市盈率(TTM)":items[9].select("span")[0].get_text(),
                   "市值":items[11].select("span")[0].get_text(),
                       }
        print(xq_news)

        #写入文件
        w.writerow(xq_news)
        print(num)
        if num >= 100:
            break
    if num >= 100:
        f.close()
        break


    #翻页
    ele = browser.find_element_by_class_name("next")
    ActionChains(browser).click(ele).perform()

