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
from lxml import etree
import json
import time

conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='test2',
        )
cur = conn.cursor()
cur.execute("select API_ID,API_Homepage from api_info ")

ret = cur.fetchall()

cur.close()
conn.commit()
conn.close()

# print ret

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
# queryStr='http://allogarage.wordpress.com/2007/11/15/api-allogarage/'
for each in ret:
    # 排除掉HOMEpage为空以及不是url形式的信息
    if json.loads(each[1]) and str(json.loads(each[1])[0]).startswith('http'):

        queryStr=json.loads(each[1])[0]
        # print json.loads(each[0])
        # print json.loads(each[1])[0]
        queryStr = urllib2.quote(queryStr)
        # print queryStr
        url = 'https://www.google.com.hk/search?q=%s&newwindow=1&safe=active&hl=en&lr=lang_en&sa=X&ved=0ahUKEwi9kcu8x-XJAhUHIqYKHW1dCfQQuAEIIA&biw=1440&bih=775' % queryStr

        request = urllib2.Request(url)
        index = random.randint(0, 9)
        user_agent = user_agents[index]
        request.add_header('User-agent', user_agent)
        response = urllib2.urlopen(request)
        html = response.read()

        selector = etree.HTML(html)
        info=selector.xpath('//*[@id="rso"]/div/div[1]/div/div/div/span/text()')
        if not info:
            info=selector.xpath('//*[@id="rso"]/div[1]/div/div/div/div/span/text()')
    
        if not info:
            info=selector.xpath('//*[@id="rso"]/div/div/div[1]/div/div/span/text()')

        print each[0],info
        

        conn= MySQLdb.connect(
                host='localhost',
                port = 3306,
                user='root',
                passwd='',
                db ='test3',
                )
        cur = conn.cursor()
        cur.execute("insert into api_google (API_ID,description) values(%s,%s)", 
                        (each[0], json.dumps(info)))

        ret = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        time.sleep(7)
# //*[@id="rso"]/div/div[1]/div/div/div/span
# //*[@id="rso"]/div[1]/div/div/div/div/span
# //*[@id="rso"]/div/div[1]/div/div/div/span