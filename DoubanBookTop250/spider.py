import requests
import re
from lxml import etree
import pymongo
from config import *
# from multiprocessing import Pool

# client = pymongo.MongoClient(MONGO_URL)
# db = client[MONGO_DB]


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response


def get_url_page(html):
    selector = etree.HTML(html.text)
    music_hrefs = selector.xpath('//a[@class="nbg"]/@href')
    comment=re.findall('<span class="inq">(.*?)</span>',html.text,re.S)
    print(comment)
    return music_hrefs


def parse_url_page(html):
    selector = etree.HTML(html.text)
    name = selector.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
    authors = re.findall('作者:.*?<a.*?href.*?>(.*?)</a>', html.text, re.S)
    if len(authors) == 0:
        author = re.findall('作者</span>:.*?<a.*?href.*?>(.*?)</a>', html.text, re.S)[0].strip()
    else:
        author = authors[0].strip()
    styles = re.findall('译者.*?<a.*?href.*?>(.*?)</a>', html.text, re.S)
    if len(styles) == 0:
        style = '中文图书'
    else:
        style = styles[0].strip()
    time = re.findall('出版年:</span>(.*?)<br/>', html.text, re.S)[0].strip()
    number = re.findall('class="rating_people.*?"v:votes">(.*?)</span>', html.text, re.S)[0].strip()+'人评论'
    source = selector.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    return {
        'name': name,
        'author': author,
        'styles': style,
        'time': time,
        'number': number,
        'source': source,
        'comment': comment
    }


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False


def main(offset):
    url = 'https://book.douban.com/top250?start=' + str(offset)
    html = get_one_page(url)
    for item in get_url_page(html):
        parse = get_one_page(item)
        result = parse_url_page(parse)
        print(result)
        # save_to_mongo(result)


if __name__ == '__main__':
    # groups = [i * 25 for i in range(GROUP_START, GROUP_END + 1)]
    # pool = Pool(1)
    # pool.map(main, groups)
    main(0)
