import requests
from lxml import etree
from bs4 import BeautifulSoup

url = "https://zhuanlan.zhihu.com/c_182712810"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.142 Safari/537.36",

}
req_content = requests.get(url, headers=headers)
soup = BeautifulSoup(req_content.content, "html.parser")
title = soup.get("#root > div > main > div > section > div > li:nth-child(1)")
print(title)
