import requests
from lxml import etree

base_url='http://www.jianshu.com/c/bDHhpK'
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
def get_html(offset):
    queries='?order_by=commented_at&page='+str(offset)
    url=base_url+queries
    print(url)
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response
    return None

def parse_html(html):
    selector=etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        auth=info.xpath('div/a/text()')[0]
        comment=info.xpath('div/p/text()')[0]
        nockname=info.xpath('div/div/a[1]/text()')[0]
        iconfont=info.xpath('div/div/a[2]/text()')[1]
        like=info.xpath('div/div/span[1]/text()')[0]
        moneys=info.xpath('div/div/span[2]/text()')
        if len(moneys)==0:
            money='0'
        else:
            money=moneys[0]
        date={
            'auth':auth,

        }
        print(auth,comment,nockname,iconfont,like,money)

def main():
    html=get_html(2)
    print(html)
    parse_html(html)

if __name__ == '__main__':
    main()

