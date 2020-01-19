import requests

# https://sffc.sh-service.com/wx_miniprogram/sites/feiguan/trashTypes_2/Handler/Handler.ashx?a=GET_KEYWORDS&kw=电池
# https://www.kancloud.cn/xika1024/lajiflw/1197404
# url2 = 'https://quark.sm.cn/api/quark_sug?q=干电池是什么垃圾'
url = 'https://laji.lr3800.com/api.php'
name = input("请输入垃圾名称:")
if len(name) == 0:
    print('垃圾名称不能为空')
params = {
    "name": name
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/76.0.3809.100 Safari/537.36 '
}
resp = requests.get(url, params=params, headers=headers)
json = resp.json()
code = json['code']
if code == 200:
    ## 垃圾分类，0 为可回收、1 为有害、2 为厨余(湿)、3 为其他(干)
    news_list = json['newslist']
    for i in news_list:
        print(i['name'])
        tp = i['type']
        if tp == 0:
            print('为可回收')
        elif tp == 1:
            print('有害垃圾')
        elif tp == 2:
            print('厨余(湿)垃圾')
        else:
            print('为其他(干)垃圾')
        print(i['explain'])
        print(i['contain'])
        print(i['tip'])
        print('\n')
else:
    print('查询失败')
