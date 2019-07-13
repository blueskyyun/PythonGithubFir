import pymysql
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import traceback
import logging
from UniversitySch.ExceptionLog import *
name = genLogName()
nm = 'DBUtil'+name
logging.basicConfig(filename=nm)

class DBUtil():
    def insertU(self,uname):
        conn = pymysql.connect(host='localhost',
                                    port=3306, user='root',
                                    passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("insert into universitylist (unname) values (%s)", uname)
            conn.commit()
        except Exception as e:
            conn.rollback()
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
    def selectU(self, uname):
        conn = pymysql.connect(host='localhost',
                               port=3306, user='root',
                               passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("select unid from universitylist where unname = %s", uname)
            data = cur.fetchone()
            if data is None:
                unid = -1
            else:
                unid = data[0]
        except Exception as e:
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
        return unid
    def inserUS(self, uname, sch_name, href):
        unid = self.selectU(uname)
        if unid is not None and unid != -1:
            conn = pymysql.connect(host='localhost',
                                   port=3306, user='root',
                                   passwd='zr1256', db='universityscholars', charset='utf8')
            cur = conn.cursor()
            try:
                cur.execute("insert into unvst_sch (unid, sch_name, href) values (%s, %s, %s)", (unid,sch_name,href))
                conn.commit()
            except Exception as e:
                conn.rollback()
                s = traceback.format_exc()
                logging.error(s)
            cur.close()
            conn.close()
    def selectUS(self, uname, sch_name):
        conn = pymysql.connect(host='localhost',
                               port=3306, user='root',
                               passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("select usid from unvst_sch where unid in (select unid from universitylist where unname = %s) and sch_name = %s", uname, sch_name)
            data = cur.fetchone()
            usid = data[0]
        except Exception as e:
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
        return usid
    def insertUSS(self, uss_name,uname, sch_name, pic_pth=' ',
                  baseinfo = ' ',joblife = '',  researchDir = ' ', reasearch_findings = ' ',
                  rFieldLabel=' ', relationShip=' ', shref = ' '):
        usid = self.selectUS(uname, sch_name)
        if usid is not None:
            conn = pymysql.connect(host='localhost',
                                   port=3306, user='root',
                                   passwd='zr1256', db='universityscholars', charset='utf8')
            cur = conn.cursor()
            try:
                cur.execute("insert into unvst_sch_scholars (uss_name,pic_pth,usid,baseinfo,joblife,researchDir,reasearch_findings,rFieldLabel,relationShip,shref) values (%s,%s,%d,%s,%s,%s,%s,%s,%s,%s)",(uss_name,pic_pth,usid,baseinfo,joblife,researchDir,reasearch_findings,rFieldLabel,relationShip,shref))
                conn.commit()
            except Exception as e:
                conn.rollback()
                s = traceback.format_exc()
                logging.error(s)
            cur.close()
            conn.close()
    def insert_unvstdetail1(self,uname,code,location):
        conn = pymysql.connect(host='localhost',
                                    port=3306, user='root',
                                    passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("insert into unvstdetail1 (unname, code, location) values (%s,%s,%s)",(uname,code,location))
            conn.commit()
        except Exception as e:
            conn.rollback()
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
    def selectUdetail1(self, uname):
        conn = pymysql.connect(host='localhost',
                               port=3306, user='root',
                               passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("select unid from unvstdetail1 where unname = %s", uname)
            data = cur.fetchone()
            if data is None:
                unid = -1
            else:
                unid = data[0]
        except Exception as e:
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()
        return unid
    def inserUdetail1S(self, uname, sch_name):
        unid = self.selectUdetail1(uname)
        if unid is not None and unid != -1:
            conn = pymysql.connect(host='localhost',
                                   port=3306, user='root',
                                   passwd='zr1256', db='universityscholars', charset='utf8')
            cur = conn.cursor()
            try:
                cur.execute("insert into unvstdetail_sch (unid, sch_name) values (%s, %s)", (unid,sch_name))
                conn.commit()
            except Exception as e:
                conn.rollback()
                s = traceback.format_exc()
                logging.error(s)
            cur.close()
            conn.close()
    # def insertUdetaileSHref(self,href):
    def inserUdetail1S2(self, uname, sch_name,href):
        unid = self.selectUdetail1(uname)
        if unid is not None and unid != -1:
            conn = pymysql.connect(host='localhost',
                                   port=3306, user='root',
                                   passwd='zr1256', db='universityscholars', charset='utf8')
            cur = conn.cursor()
            try:
                cur.execute("insert into unvstdetail_sch2 (unid, sch_name,href) values (%s, %s,%s)", (unid, sch_name,href))
                conn.commit()
            except Exception as e:
                conn.rollback()
                s = traceback.format_exc()
                logging.error(s)
            cur.close()
            conn.close()
    def insert_unvstdetail3(self,uname,code,location):
        conn = pymysql.connect(host='localhost',
                                    port=3306, user='root',
                                    passwd='zr1256', db='universityscholars', charset='utf8')
        cur = conn.cursor()
        try:
            cur.execute("insert into unvstdetail3 (unname, code, location) values (%s,%s,%s)",(uname,code,location))
            conn.commit()
        except Exception as e:
            conn.rollback()
            s = traceback.format_exc()
            logging.error(s)
        cur.close()
        conn.close()




