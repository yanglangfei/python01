import requests
from bs4 import BeautifulSoup as bs
import pymysql
import time
import random

url = 'https://www.pythontab.com/html/pythonhexinbiancheng/'

config = {
    'host': '192.168.101.103',
    'port': 3306,
    'user': 'python',
    'password': 'admin123',
    'database': 'test',
    'charset': 'utf8'
}


def get_list(get_url):
    resp = requests.get(get_url)
    return resp.content.decode('utf-8')


def get_content(link):
    resp = requests.get(link)
    return resp.content.decode('utf-8')


def parse_content(html):
    soup = bs(html, "html.parser")
    return soup.find(id='Article')


def parse_html(html):
    lst = []
    soup = bs(html, 'html.parser')
    li = soup.find(id='catlist').find_all('li')
    for i in li:
        title = i.find('h2').find('a').get_text()
        link = i.find('h2').find('a')['href']
        cont = parse_content(get_content(link))
        desc = i.find('p').get_text()
        list_item = (title, desc, cont)
        lst.append(list_item)
    return lst


def save_data(data):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    for i in data:
        sql = ("insert into article(title,descript,content) values (%s,%s,%s)")
        data = (i[0], i[1], str(i[2]))
        cur.execute(sql, data)

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    for i in range(1, 28):
        if i == 1:
            get_url = url
        else:
            get_url = url + "{}.html".format(str(i))
        content = get_content(get_url)
        lst = parse_html(content)
        save_data(lst)
        print("save " + str(i) + " page")
        time.sleep(random.randint(1, 3))
