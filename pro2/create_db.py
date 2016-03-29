#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-07 10:32:36
# @Author  : jiong (447991103@qq.com)
# @Version : $Id$

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import MySQLdb
import subprocess
import os
os.system('net start mysql')
subprocess.Popen(['mysql','-uroot',])
# subprocess.Popen(['CREATE DATABASE `test2` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'])
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='jiong_test',
        )
cur = conn.cursor()

#创建数据表
# cur.execute("CREATE DATABASE test1 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci")

cur.execute("DROP TABLE IF EXISTS api_info")
cur.execute("DROP TABLE IF EXISTS api_followers")
cur.execute("DROP TABLE IF EXISTS api_mushup")
cur.execute("create table api_info(API_Name varchar(200) ,\
									API_ID varchar(20),\
									Description varchar(3000),\
									Primary_Category varchar(100),\
									Secondary_Categories varchar(300),\
									Followers_Number varchar(30),\
									API_Homepage varchar(300),\
									API_Provider varchar(300))")
cur.execute("create table api_followers(API_ID varchar(20) ,\
									Followers_Name varchar(3000) )")
cur.execute("create table api_mushup(API_ID varchar(20) ,\
									  mushup_name varchar(3000))")


cur.close()
conn.commit()
conn.close()

