import os
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


def download_img_from_path(number, save_path):
    # raw_input 不管用户输入什么 转换为字符串
    keyword = raw_input("输入关键字: ")

    # 向指定地址发起GET请求
    requests_content = requests.get('http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2'
                                    '&nc=1&ie=utf-8&word=' + keyword)
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
