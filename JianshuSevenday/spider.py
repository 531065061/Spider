import requests
from lxml import etree
import re
import time
import pymongo

homepage_url = 'http://www.jianshu.com'
base_url = 'http://www.jianshu.com/trending/weekly'

client = pymongo.MongoClient('192.168.66.129:27017')
db = client['JianshuSevenday']
MONGO_TABLE = 'JianshuSevenday'


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        return None


def get_other_html(offset, data_note_id):
    seen_snote_ids_param = '?seen_snote_ids%5B%5D=' + '&seen_snote_ids%5B%5D='.join(data_note_id)
    html_url = base_url + seen_snote_ids_param + '&page=' + str(offset)
    return get_html(html_url)


def get_url_param(html):
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        article_url_part = info.xpath('div/a/@href')[0]
        yield [article_url_part]


def get_html_param(html):
    selector = etree.HTML(html.text)
    data_note_id = selector.xpath('//li/@data-note-id')
    return data_note_id


def parse_url(html):
    selector = etree.HTML(html.text)
    urls = selector.xpath('//meta[@name="mobile-agent"]/@content')
    author = selector.xpath('//span[@class="name"]/a/text()')[0]
    article = selector.xpath('//h1[@class="title"]/text()')[0]
    date = selector.xpath('//span[@class="publish-time"]/text()')[0]
    word = selector.xpath('//span[@class="wordage"]/text()')[0]
    view = re.findall('"views_count":(.*?),', html.text, re.S)[0]
    comment = re.findall('"comments_count":(.*?),', html.text, re.S)[0]
    like = re.findall('"likes_count":(.*?),', html.text, re.S)[0]
    url = re.findall('url=(.*?)\'', str(urls))[0]

    info = {
        'url': url,
        'author': author,
        'article': article,
        'date': date,
        'word': word,
        'view': view,
        'comment': comment,
        'like': like,
    }
    # save_to_mongo(info)
    return info


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False


def main(offset):
    html = get_html(base_url)
    for items in get_url_param(html):
        for item in items:
            url = homepage_url + item
            parse_html = get_html(url)
            result = parse_url(parse_html)
            save_to_mongo(result)

    data_note_id = get_html_param(html)
    for i in range(2, offset):
        html = get_other_html(i, data_note_id)
        data_note_id.extend(get_html_param(html))
        for items in get_url_param(html):
            for item in items:
                url = homepage_url + item
                parse_html = get_html(url)
                time.sleep(2)
                result = parse_url(parse_html)
                save_to_mongo(result)


if __name__ == '__main__':
    main(3)
