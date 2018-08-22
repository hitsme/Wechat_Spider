#!usr/bin/python3
#-*- coding:UTF-8 -*-
import pymysql as MySQLdb
def getConnectDB():
    db= MySQLdb.connect(host = '45.62.226.188', port = 3306, user = 'root', passwd = 'password', db = 'youtubeclub', charset="utf8")

    return db
def initWeChatSpiderLog():
    db=getConnectDB()
    cursor=db.cursor()
    createSql="""create table if not exists WechatSpider_log(wechatid varchar(50) not null primary key ,aid varchar(100),atitle TEXT,spiderdate datetime,fornumname varchar(200),fornumid varchar(50),isDelete char(5))
    """
    cursor.execute(createSql)
    db.commit()
    db.close()
    return

def initSpiderRecord():
    db=getConnectDB()
    cursor=db.cursor()
    initSql="""create table if not exists Spider_Record(spiderUrl TEXT,fornumname varchar(500)
,isEnable char(5))"""
    cursor.execute(initSql)
    db.commit()
    db.close()
    return