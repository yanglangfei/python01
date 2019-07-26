import os
import random
import threading
import time
import ssl

import requests
from bs4 import BeautifulSoup

meizi2_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 "
    "Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 "
    "Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
]

mziTu = 'http://www.mzitu.com/'


def download_page(url):
    # 用于下载页面
    headers = {'User-Agent': random.choice(meizi2_headers)}
    r = requests.get(url, headers=headers)
    return r.text


def get_pic_list(html, cur_page):
    create_dir('pic/' + cur_page)
    # 获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find(id="pins").find_all("li")
    for i in pic_list:
        link = i.find('a').get('href')  # 套图链接
        text = i.find('span').get_text()  # 套图名字
        print("link:" + link + "  title:" + text)

        #  for j in range(0, 50):
        #     if j == 0:
        #        url = link
        #   else:
        #      url = link + "/" + str(j)
        #  try:
        #     print("下载页面:" + url)
        html = download_page(link)  # 下载界面
        get_pic(html, text,cur_page)
    # finally:
    #   print("error:" + str(j))
    #  break


def get_pic(html, text,cur_page):
    soup = BeautifulSoup(html, 'html.parser')
    pic = soup.find('div', class_="main-image").find('img').get('src')  # 找到界面所有图片
    # create_dir('pic/{}'.format(text))
    # for i in pic_list:
    #    pic_link = i.get('src')  # 拿到图片的具体 url

    headers = {'User-Agent': random.choice(meizi2_headers), 'Referer': pic}
    r = requests.get(pic, headers=headers)  # 下载图片，之后保存到文件
    array = pic.split('/')
    file_name = array[len(array) - 1]
    file_path = 'pic/' + cur_page + "/" + file_name
    with open(file_path, "wb") as f:
        f.write(r.content)
        f.close()
        time.sleep(random.randint(1, 3))


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def execute(url, cur_page):
    page_html = download_page(url)
    get_pic_list(page_html, cur_page)


def main():
    queue = [i for i in range(1, 72)]  # 构造 url 链接 页码。
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 5 and len(queue) > 0:  # 最大线程数设置为 5
            cur_page = queue.pop(0)
            if cur_page == 1:
                url = mziTu
            else:
                url = mziTu + 'page/' + str(cur_page)
            thread = threading.Thread(target=execute, args=(url, str(cur_page)))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()
