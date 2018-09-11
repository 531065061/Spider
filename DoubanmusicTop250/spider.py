import requests
from lxml import etree


def get_url_page():
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
    html=requests.get(url,headers=headers)
    print(html)

def parse_one_page():
    selector=etree.HTML(html.text)
    music_hrefs=selector.xpath('//a[@class="nbg"]/@href')
    print(music_hrefs)
    # for music_href in music_hrefs:
    #     get_music_info(music_href)

if __name__=='__main__':
    url='https://music.douban.com/top250?start=25'
    html=get_url_page()
    aaa=parse_one_page()