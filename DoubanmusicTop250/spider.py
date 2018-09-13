import requests
import re
from lxml import etree
import pymongo
from config import *

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def get_one_page(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    response=requests.get(url,headers=headers)
    return response

def get_url_page(html):
    selector=etree.HTML(html.text)
    music_hrefs=selector.xpath('//a[@class="nbg"]/@href')
    return music_hrefs

def parse_url_page(html):
    selector=etree.HTML(html.text)
    name=selector.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
    author = re.findall('表演者:.*?>(.*?)</a>',html.text,re.S)[0]
    styles = re.findall('<span class="pl">流派:</span>&nbsp;(.*?)<br />',html.text,re.S)[0]
    if len(styles) == 0:
        style = '未知'
    else:
        style = styles[0].strip()
    time = re.findall('发行时间:</span>&nbsp;(.*?)<br />',html.text,re.S)[0].strip()
    # publishers = re.findall('出版者:.*?>(.*?)</a>',html.text,re.S)
    number = re.findall('class="rating_people.*?"v:votes">(.*?)</span>',html.text,re.S)
    if len(number) == 0:
        number = '未知'
    else:
        number = number[0].strip()+'人评论'
    source=selector.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    # print(name, author, style, time, number,source)
    return {
        'name':name,
        'author':author,
        'styles':styles,
        'time':time,
        'number':number,
        'source':source
    }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到MongoDB成功',result)
        return True
    return False

def main(offset):
    url='https://music.douban.com/top250?start='+str(offset)
    html=get_one_page(url)
    for item in get_url_page(html):
        parse=get_one_page(item)
        result=parse_url_page(parse)
        print(result)
        save_to_mongo(result)

        # parse_url_page(get_one_page(item))

if __name__=='__main__':
    for i in range(2):
        main(i*25)