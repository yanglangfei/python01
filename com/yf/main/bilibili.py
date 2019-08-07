import json
import re
import requests
import threading
import time
import random


def parse_live_list(content):
    results = content["result"]
    lst = []
    for i in results:
        live_item = (i["arcurl"], i["tag"], i["title"], i["pic"], i["author"])
        lst.append(live_item)
    return lst


def get_live_link(content):
    pattern = "<script>window.__playinfo__=(.*?)</script>"
    result = re.findall(pattern, content)[0]
    temp = json.loads(result)
    data = temp["data"]
    try:
        for item in data['durl']:
            if 'url' in item.keys():
                video_url = item['url']
                return video_url
    except Exception as e:
        print("异常")


class Bilibili(threading.Thread):
    def __init__(self, url, i):
        threading.Thread.__init__(self)
        self.url = url
        self.page = i
        self.getHtmlHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'
        }

        self.downloadVideoHeaders = {
            'Origin': 'https://www.bilibili.com',
            'Referer': 'https://www.bilibili.com/video/av26522634',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/69.0.3497.100 Safari/537.36',
        }

    def get_live_list(self):
        return requests.get(self.url, headers=self.getHtmlHeaders).json()

    def get_live_info(self, page_link):
        resp = requests.get(page_link, headers=self.getHtmlHeaders)
        return resp

    def run(self):
        json_content = self.get_live_list()
        lst = parse_live_list(json_content)
        try:
            for i in lst:
                page_resp = self.get_live_info(i[0])
            live_link = get_live_link(page_resp.content.decode("utf-8"))
            title = re.sub(r'[\/:*?"<>|]', '-', i[2])  # 去掉创建文件时的非法字符
            filename = title + '.flv'
            print("download:" + filename + "  url:" + live_link)
            with open("D:/bilibili/" + filename, "wb") as f:
                f.write(
                    requests.get(url=live_link, headers=self.downloadVideoHeaders, stream=True, verify=False).content)
        except Exception:
            print("异常...")
        print("download " + str(self.page) + "页")


if __name__ == '__main__':
    for i in range(1, 20):
        url = "https://s.search.bilibili.com/cate/search?search_type=video&view_type=hot_rank&cate_id=28&page={" \
              "}&pagesize=20" \
              "&jsonp=jsonp&time_from=20190731&time_to=20190807&keyword=古风".format(str(i))
        Bilibili(url, i).start()
        time.sleep(random.randint(1, 3))
