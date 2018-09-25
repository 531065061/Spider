import requests
from lxml import etree
import re

homepage_url='http://www.jianshu.com'
base_url='http://www.jianshu.com/trending/weekly'

def get_html(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response
    else:
        return None

def get_url(html):
    selector=etree.HTML(html.text)
    infos=selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        article_url_part=info.xpath('div/a/@href')[0]
        yield [article_url_part]

def parse_url(html):
    selector=etree.HTML(html.text)
    author = selector.xpath('//span[@class="name"]/a/text()')[0]
    article = selector.xpath('//h1[@class="title"]/text()')[0]
    date = selector.xpath('//span[@class="publish-time"]/text()')[0]
    word = selector.xpath('//span[@class="wordage"]/text()')[0]
    view = re.findall('"views_count":(.*?),',html.text,re.S)[0]
    comment = re.findall('"comments_count":(.*?),',html.text,re.S)[0]
    like = re.findall('"likes_count":(.*?),',html.text,re.S)[0]
    print(author,article,date,word,view,comment,like)
    # print(author)

def main():
    html=get_html(base_url)
    for items in get_url(html):
        for item in items:
            url=homepage_url+item
            parse_html=get_html(url)
            parse_url(parse_html)

if __name__=='__main__':
    main()