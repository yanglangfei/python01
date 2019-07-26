import os
import random
import uuid
import requests  # 网络请求
import urllib
import re
import time
import bs4  # 解析 HTML

# number :下载个数
# path : 下载地址
# save_path :保存地址
from pip._vendor.distlib.compat import raw_input


bz_headers = [
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


def download_img_from_path(number, save_path):
    # raw_input() 不管用户输入什么 转换为字符串
    # input() 输入什么类型就是什么类型
    keyword = raw_input("输入关键字: ")
    headers = {'User-Agent': random.choice(bz_headers), 'Referer': "http://image.baidu.com"}    # 向指定地址发起GET请求
    requests_content = requests.get('http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2'
                                    '&nc=1&ie=utf-8&word=' + keyword, headers)
    # 实际请求地址
    url = requests_content.url
    # 请求 byte 对象
    content = requests_content.content
    text = requests_content.text
    # 设置编码
    # requests_content.encoding = "utf-8"
    # 检查出错  出错抛异常
    # requests_content.raise_for_status()

    # 使用  bs4 解析元素
    # soup = bs4.BeautifulSoup(requests_content.text, "html.parser")
    # put = soup.select('input[type="submit"]')
    # input_value = put[0].get('value')
    # print(input_value)

    # 创建文件夹
    # os.makedirs("work")
    # 构建文件路径
    # os.path.join("a", "b", "c")
    # 获取文件基本名称
    # os.path.basename("c")
    file_name = "bz"
    path = save_path + keyword + "/"

    is_exists = os.path.exists(path)

    if not is_exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print("create path")
    else:
        print("path exists")

    # 使用正则化方法分析出图片地址

    img_url = re.findall('"objURL":"(.*?)",', requests_content.text, re.S)
    for i in range(number):
        # 保存图片
        t = time.time()

        file_name = file_name.join(str(uuid.uuid1()).split("_"))

        urllib.request.urlretrieve(img_url[i], path + file_name + '.jpg')
        print('地址为：' + img_url[i])


if __name__ == '__main__':
    download_img_from_path(10, 'd:/壁纸/')
