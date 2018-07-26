# encoding: utf-8
from http.cookiejar import MozillaCookieJar, CookieJar
from urllib.request import Request, build_opener, HTTPCookieProcessor, urlopen
import  json
from JsonTools import jsonString2Dict
from DBDao import getConnectDB
from DBDao import initSpiderRecord
from DBDao import initWeChatSpiderLog
from publishDiscuzMethods import publishWebsite
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
DEFAULT_TIMEOUT = 360


def gen_login_cookie():
    cookie = MozillaCookieJar()
    cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)
    return cookie

def grabContent(cookie,url):
    req = Request(url, headers=DEFAULT_HEADERS)
    opener = build_opener(HTTPCookieProcessor(cookie))
    response = opener.open(req, timeout=DEFAULT_TIMEOUT)
    encode_json = response.read().decode("utf8")
    decode_json = jsonString2Dict(encode_json)
    return decode_json
def grab(cookie):
 db=getConnectDB()
 cursor=db.cursor()
 spiderSql='select spiderurl,fornumname from Spider_Record where isenable="1"'
 cursor.execute(spiderSql)
 spiderlist=cursor.fetchall()
 for j in spiderlist:
    req = Request(str(j[0]), headers=DEFAULT_HEADERS)
    opener = build_opener(HTTPCookieProcessor(cookie))
    response = opener.open(req, timeout=DEFAULT_TIMEOUT)
    encode_json=response.read().decode("utf8")
    decode_json=jsonString2Dict(encode_json)
    print(decode_json['app_msg_cnt'])
    endIndex=int(decode_json['app_msg_cnt'])
    db=getConnectDB()
    cursor=db.cursor()
    while endIndex>=0:
      spiderUrl=str(j[0]).replace('begin=0','begin='+str(endIndex))
      decode_json=grabContent(cookie,spiderUrl)
      for i in decode_json['app_msg_list']:
        cursor.execute('select count(*) from WechatSpider_log where aid="' +i['aid']+'"')
        cnt=cursor.fetchone()[0]
        if cnt==0:
            publishWebsite(str(i['aid']),str(i['digest']),str(i['link']),str(j[1]))
      endIndex -= 6
    response.close()
    db.close()



def start():
    cookie = gen_login_cookie()
    grab(cookie)
    cookie.save(filename='./cookies.txt',ignore_discard=True, ignore_expires=True)


if __name__ == '__main__':
    #initWeChatSpiderLog()
    #initSpiderRecord()
    start()