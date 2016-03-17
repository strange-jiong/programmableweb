#!/usr/bin/env python
#-*- coding:utf-8 -*-
# @Date    : 2015-12-11 11:37:16
# @Author  : jiong (447991103@qq.com)
# @Version : $Id$

import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import MySQLdb
import requests,urllib2,random
import json

print '123'
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='test2',
        )
cur = conn.cursor()
cur.execute("select API_ID,Primary_Category,Secondary_Categories from api_info")

ret = cur.fetchall()
print ret[0]
print ret[0]
jiong=open('test3.txt','w')
# jiong1=open('test4.txt','w')
n=0
tem=['Mapping','Social','eCommerce','Tools','Search','Mobile','API','Video','Messaging','Financial']
try:
	for each in ret:
		if json.loads(each[1]) :
			col1=json.loads(each[0])
			col2=json.loads(each[1])[0]
			# print len(each)
			if len(each)==3:
				try:
					col3=json.loads(each[2])
				except Exception,e:
					col3=[]
					print 'error!!!!!',e
				finally:
					pass
			# if col2=='Mapping' or col2=='Social' or col2=='eCommerce' or col2=='Tools' or col2=='Search' or col2=='Mobile' or col2=='API' or col2=='Video' or col2=='Messaging' or col2=='Financial':
			else:
				col3=[]

			
			col3.append(col2)
			for a in col3:
				# print a
				if a in tem:	
					jiong.write(col1+'\t'+a+'\n')
					n+=1
					# continue
					break
			# jiong1.write(col2+'\t'+col1+'\n')
	jiong.write(str(n))
	jiong.close()
	print n
except Exception,e:
	print 'error!!!!!',e

# jiong1.close()