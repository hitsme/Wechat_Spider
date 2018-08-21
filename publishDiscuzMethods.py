#!/usr/bin/python3
# #-*-coding:utf-8-*-
from DBDao import getConnectDB
import datetime
import time
import traceback
import uuid
def getContent(atitle,alink):
    #缤纷花食，悄悄挖掘玫瑰的不同吃法[mp4]http://45.62.226.188/缤纷花食，悄悄挖掘玫瑰的不同吃法.mp4[/mp4]
    return str(atitle)+'  [href]'+alink+'[/href]'
def getTid(cursor):
    cursor.execute('select tid from pre_forum_post order by tid desc limit 0,1')
    return cursor.fetchone()[0]

def getFid(cursor,fornumname):
    try:
        cursor.execute('select fid from pre_forum_forum where name="'+fornumname+'"')
        fid=cursor.fetchone()[0]
        return fid
    except:
        print('function getFid() error')
def publishWebsite(aid,atitle,alink,fornumname):
    db=getConnectDB()
    cursor=db.cursor()
    try:
      cursor.execute('select pid from pre_forum_post order by pid desc limit 0,1')
      lastPid=cursor.fetchone()[0]
      lastPid+=1
      print(lastPid)
      fid=getFid(cursor,fornumname)
      tid=getTid(cursor)
      tid+=1
      timeminute=time.time()
      cursor.execute("""insert into pre_forum_post(pid, fid, tid,first, author,
                                                  authorid,subject,dateline,message,useip,
                                                  port,invisible,anonymous,usesig,htmlon,
                                                  bbcodeoff,smileyoff,parseurloff,attachment,rate,
                                                  ratetimes,position) 
                                                  values("%s","%s","%s","%s","%s",
                                                         "%s","%s","%s","%s","%s",
                                                         "%s","%s","%s","%s","%s",
                                                         "%s","%s","%s","%s","%s",
                                                         "%s","%s")"""
                                                  %(lastPid,fid,tid,'1','admin',
                                                    '1',atitle,str(timeminute),getContent(atitle,alink),'127.0.0.1',
                                                    '740','0','0','1','0',
                                                    '0','-1','0','0','0',
                                                    '0','1'))
      cursor.execute("""insert into  pre_forum_thread(tid,fid,posttableid,typeid,sortid,readperm,price,author,authorid,subject,dateline, lastpost,lastposter,views,replies,displayorder,highlight,digest,rate,special,attachment,moderated,closed,stickreply,recommends,recommend_add,recommend_sub,heats,status,isgroup,favtimes,sharetimes,stamp,icon,pushedaid,cover,replycredit) 
VALUES("%s" ,"%s", 0, 0, 0, 0, 0, 'admin', 1, "%s","%s", "%s", "admin", 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,32, 0, 0, 0, -1, -1, 0, 0, 0)"""%(tid,fid,atitle,str(timeminute),str(timeminute)))
      cursor.execute("""insert into pre_forum_post_tableid(pid) values("%s")"""%(lastPid))
      #"UPDATE `pre_forum_forum` SET threads=threads+1, posts=posts+1,todayposts=todayposts+1 ,lastpost='" + currentPId + " " + rss.getTitle() + " " + time + " 狂飙蜗牛" + "' WHERE fid=" + fid;
      cursor.execute('UPDATE pre_forum_forum SET threads=threads+1, posts=posts+1,todayposts=todayposts+1 ,lastpost="' + str(lastPid) + ' ' + atitle + ' ' +str(timeminute) + ' admin' + '" WHERE fid=' + str(fid))
      writeWechatSpiderLog(aid,atitle,fid,fornumname)
      db.commit()
    except Exception as e:
      print(e)
      print ('function publishWebsite error')
    finally:
        db.close()
    return

def writeWechatSpiderLog(aid,atitle,fornumid,fornumname):
    db=getConnectDB()
    cursor=db.cursor()
    try:
        dldate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("""insert into WechatSpider_log(wechatid,aid,atitle,fornumname,fornumid,spiderdate)
 values("%s","%s","%s","%s","%s","%s")"""%(str(uuid.uuid1()),aid,atitle,fornumname,fornumid,str(dldate)))
        cursor.execute("""insert into WechatSpider_log(wechatid,aid,atitle,fornumname,fornumid,spiderdate)
 values("%s","%s","%s","%s","%s","%s")"""%(str(uuid.uuid1()),aid,atitle,fornumname,fornumid,str(dldate)))

        db.commit()
    except :
        traceback.print_exc()
        print ('function write WechatSpider_log error')
    finally:
        db.close()
    return