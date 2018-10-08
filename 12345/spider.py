#-*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import http.cookiejar
from json import loads

c=http.cookiejar.LWPCookieJar()
cookie=urllib.request.HTTPCookieProcessor(c)
opener=urllib.request.build_opener(cookie)

def login():
    req=urllib.request.Request('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.5748421704037432')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    code_image=opener.open(req).read()
    with open('code.png','wb') as fn:
        fn.write(code_image)
    req=urllib.request.Request('https://kyfw.12306.cn/passport/captcha/captcha-check')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    code=input('请输入验证码:')
    date={
    'answer': code,
    'login_site': 'E',
    'rand': 'sjrand'
    }
    date=urllib.parse.urlencode(date).encode(encoding='utf-8')
    res=opener.open(req,data=date)
    html=res.read().decode('utf-8')
    # result=loads(html)
    # if result['result_code']=='4':
    #     print('验证通过')
    # else:
    #     print('验证码校验失败')
    print(html)


login()