import requests

url = 'http://douyin.bm8.com.cn/'
resp = requests.get(url)
print(resp.text)
