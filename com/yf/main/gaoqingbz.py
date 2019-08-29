import requests
from lxml import etree
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                  'Safari/537.36 '
}
url = 'https://www.pexels.com/search/Scenery/'
res = requests.get(url, headers=headers)
html = etree.HTML(res.text)
infos = html.xpath('//div[@class="photos__column"]/div')
if not os.path.exists('bizhi'):
    os.makedirs('bizhi')

for info in infos:
    img = info.xpath('article/a[1]/img/@src')
    if len(img) == 1:
        img = img[0]
        print(img)
        data = requests.get(img, headers=headers)
        f = open('bizhi/' + img.split('?')[0][-11:], 'wb')
        f.write(data.content)
        f.flush()
