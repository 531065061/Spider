import requests
from lxml import etree

base_url='http://www.jianshu.com/c/bDHhpK'
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}
def get_html(offset):
    queries='?order_by=commented_at&page='+str(offset)
    url=base_url+queries
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response
    return None

def parse_html(html):
    selector=etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="note-list"]/li')
    for info in infos:
        auth=info.xpath('div/div[1]/div/a/text()')[0]
        print(auth)

def main():
    html=get_html(2)
    print(html)
    parse_html(html)

if __name__ == '__main__':
    main()

