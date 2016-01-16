# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals  # ,log
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class Pro2Pipeline(object):
	
	def __init__(self):
		self.conn = MySQLdb.connect(
			host='localhost',
			port=3306,
			user='root',
			passwd='',
			db='test2',
		)
		self.conn.set_character_set('utf8')
		self.cur = self.conn.cursor()

	def process_item(self, item, spider):
		# 2,3,12
		# 这里存在一个序列化保存的问题，因为mysql支持的保存类型并没有，所以需要进行序列化来保存数据结构的类型
		# 判断item的长度  存入不同的表中
		if 'Followers_Name' in item.keys():
			self.cur.execute("insert into api_followers (API_ID,Followers_Name) values(%s,%s)", 
				(json.dumps(item['API_ID']), json.dumps(item['Followers_Name'])))
			print item
		elif 'mushup_name' in item.keys() :

			self.cur.execute("insert into api_mushup (API_ID,mushup_name) values(%s,%s)",
							 (json.dumps(item['API_ID']),
							  json.dumps(item['mushup_name'])
							  ))
			print item
		else:
			self.cur.execute("insert into api_info (API_Name,\
				API_ID,\
				Description,\
				Primary_Category,\
				Secondary_Categories,\
				Followers_Number,\
				API_Homepage) \
				values(%s,%s,%s,%s,%s,%s,%s)",
							 (json.dumps(item['API_Name']),
							  json.dumps(item['API_ID']),
							  json.dumps(item['Description']),
							  json.dumps(item['Primary_Category']),
							  json.dumps(item['Secondary_Categories']),
							  json.dumps(item['Followers_Number']),
							  json.dumps(item['API_Homepage'])
							  ))
			print item
		# self.cur.close()
		self.conn.commit()
		# self.conn.close()
		# return item

