import requests
from lxml import etree
import time
import pymongo
from config import *

base_url = 'http://www.jianshu.com/c/bDHhpK'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def get_html(offset):
    queries = '?order_by=commented_at&page=' + str(offset)
    url = base_url + queries
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    return None


def parse_html(html):
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        url = info.xpath('div/a/@href')[0]
        auth = info.xpath('div/a/text()')[0].strip()
        comment = info.xpath('div/p/text()')[0].strip()
        nockname = info.xpath('div/div/a[1]/text()')[0].strip()
        iconfont = info.xpath('div/div/a[2]/text()')[1].strip()
        like = info.xpath('div/div/span[1]/text()')[0].strip()
        moneys = info.xpath('div/div/span[2]/text()')
        if len(moneys) == 0:
            money = '无'
        else:
            money = moneys[0]

        date = {
            'url': 'http://www.jianshu.com' + url,
            'auth': auth,
            'comment': comment,
            'nockname': nockname,
            'iconfont': iconfont,
            'like': like,
            'money': money
        }
        save_parse(date)


def save_parse(result):
    if db[MONGO_TABLE].insert_one(result):
        print('存储到MongDB成功', result)
        return True
    return False


def main(offset):
    html = get_html(offset)
    parse_html(html)
    time.sleep(2)


if __name__ == '__main__':
    for offset in range(1, 10):
        main(offset)
