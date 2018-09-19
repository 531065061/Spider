import requests
import re
import pymysql
from config import *

conn = pymysql.connect(**MYSQL)

cursor = conn.cursor()


def get_one_page():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page():
    pattern = re.compile(
        '<a class="nbg".*?<img src="(.*?)" width="90" />'
        + '.*?a href="(.*?)" onclick=&#34;'
        + '.*?&#34; title="(.*?)"'
        + '.*?<span style="font-size:12px;">(.*?)</span>'
        + '.*?<p class="pl">(.*?)</p>'
        + '.*?<span class="pl">\((.*?)\)</span>'
        + '.*?<span class="inq">(.*?)</span>'
        , re.S)
    items = re.findall(pattern, html)
    print(items)
    for item in items:
        yield {
            'images': item[0],
            'url': item[1],
            'title': item[2] + ' 又名' + item[3],
            'actor': item[4].replace('&nbsp;', '').replace('<br>\n', '').replace(' ', '').strip(),
            'score': item[5].replace('\n', '').replace(' ', '').strip(),
            'comment': item[6]
        }


def save_to_mysql():
    # cursor.execute("""create database if not exists doubanbooktop250 character set utf8""")
    sql_createTb = """create TABLE if not exists doubanbooktop250 (
                     id int auto_increment,
                     url  char (255),
                     images char (255),
                     title char (255),
                     actor char (255),
                     score char (255),
                     comment char (255),
                     primary key (id))
                     default charset=utf8;
                     """
    table = "doubanbooktop250"
    cols = item.keys()
    vals = item.values()
    # cursor.execute(sql_createTb)
    sql_inset = "insert into %s (%s) values(%s)" % (
        table, ",".join(cols), ",".join(['%s'] * len(item)))
    cursor.execute(sql_inset, list(item.values()))
    # cursor.close()
    conn.commit()
    # conn.close()


if __name__ == '__main__':
    offsets = (i * 25 for i in range(2))
    for offset in offsets:
        urls = ['http://book.douban.com/top250?start=' + str(offset) + '&filter=']
        for url in urls:
            html = get_one_page()
            parse_one_page()
            for item in parse_one_page():
                print(item)
                save_to_mysql()
