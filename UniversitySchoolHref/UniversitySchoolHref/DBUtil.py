import pymysql
import traceback
import logging
from UniversitySchoolHref.ExceptionLog import *
name = genLogName()
nm = 'DBUtil'+name
logging.basicConfig(filename=nm)
class DBUtil():
    def updateSchHref(self,usid, href):
        conn = pymysql.connect(host='localhost',
                               port=3306, user='root',
                               passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("update unvstdetail_sch3 set href = %s where usid = %s", (href,usid))
            conn.commit()
        except Exception as e:
            conn.rollback()
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
    def selectByUsid(self, usid):
        conn = pymysql.connect(host='localhost',
                               port=3306, user='root',
                               passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("select * from unvstdetail_sch3 where usid = %s", usid)
            data = cur.fetchone()
        except Exception as e:
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
        return data
    def select_unvstdetail3(self,unid):
        conn = pymysql.connect(host='localhost',
                               port=3306, user='root',
                               passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("select unname from unvstdetail3 where unid = %s", unid)
            data = cur.fetchone()
        except Exception as e:
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
        return data

