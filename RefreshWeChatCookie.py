#!/usr/bin/python3
#-*- coding:utf-8 -*-
from http.cookiejar import MozillaCookieJar, CookieJar
from urllib.request import Request, build_opener, HTTPCookieProcessor, urlopen
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
DEFAULT_TIMEOUT = 360
def gen_login_cookie():
    cookie = MozillaCookieJar()
    cookie.load('/www/wwwroot/youtube.club/upload/wechat_spider/cookies.txt', ignore_discard=True, ignore_expires=True)
    return cookie

def get(url,cookie):
    handler = HTTPCookieProcessor(cookie)
    opener = build_opener(handler)
    req = Request(url, headers=DEFAULT_HEADERS)
    response = opener.open(req, timeout=DEFAULT_TIMEOUT)
    #print (response.read().decode('utf-8'))
    cookie.save(filename='/www/wwwroot/youtube.club/upload/wechat_spider/cookies.txt', ignore_discard=True, ignore_expires=True)
    response.close()
def start():
    cookie = gen_login_cookie()
    get('https://mp.weixin.qq.com',cookie)


if __name__=='__main__':
    start()
