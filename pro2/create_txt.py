#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Date    : 2015-12-11 11:37:16
# @Author  : jiong (447991103@qq.com)
# @Version : $Id$

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests
import urllib2
import random
import json


conn = MySQLdb.connect(
    host='10.13.75.146',
    port=3306,
    user='root',
    passwd='',
    db='api',
)
cur = conn.cursor()
cur.execute(
    "select Description,Primary_Category,Secondary_Categories from api_info")

ret = cur.fetchall()
print 'length:', len(ret)

jiong = open('test.txt', 'w')
# jiong1=open('test2.txt','w')
count = []
tag_num = 0
# 得去掉description中间的空行
for each in ret[:200]:
    try:
        if json.loads(each[1]):
            col1 = json.loads(each[0])
            col1=col1.replace('\r','').replace('\n','').replace('\t','')
            primary = json.loads(each[1])
            secondary = json.loads(each[2])
            temp = []
            for a in primary:
                temp.append(a)
            for b in secondary:
                temp.append(b)
            for c in temp:
                if c not in count:
                    tag_num += 1
                    count.append(c)
            lable = ','.join(temp)
            jiong.write('[' + lable + ']' + '\t' + col1 + '\n')
            # jiong1.write(col2+'\t'+col1+'\n')
    except Exception:
        pass
print 'tag_num:', tag_num, len(count)
jiong.close()
# jiong1.close()


cur.close()
conn.commit()
conn.close()
