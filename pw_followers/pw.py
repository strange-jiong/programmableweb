# -*- coding: utf-8 -*-

import urllib
import urllib2
import requests
import cookielib
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""
entrance
http://www.programmableweb.com/category/all/apis

destination
http://www.programmableweb.com/api/forecast/followers

爬取pw网站的api的followers信息
"""


def get_api_name(url):
    """
    获取每一页上的api的name
    """
    print '正在获取api_name...'
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(url)
    html = response.read()
    api_name = re.findall(r'    <a href="/api/(.+?)">', html)
    # print api_name
    return api_name
    # pass


def get_followers(name):

    print '正在获取%s的followers...' % name
    url = "http://www.programmableweb.com/api/%s/followers" % name
    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(url)
    html = response.read()
    followers = re.findall(r'  <a href="/profile/(.+?)"><img src=', html)
    followers_num = int(re.findall(
        r"<div class='block-title'><span>Followers \((.+?)\)", html)[0])
    print 'followers_num:', followers_num
    # print followers
    # print len(followers)
    return followers, followers_num, opener


def get_followers_more(api_name, followers_num, opener):
    """
    如果超过一页所能显示的量(100个)，则继续执行此函数
    """
    print 'followers_num多余100，正在获取%s的其余follwers' % api_name
    url = 'http://www.programmableweb.com/api/%s/followers?pw_view_display_id=list_all&page=' % name
    followers_url = [url + '%d' %
                     num for num in range(1, followers_num / 100 + 2)]
    followers = []
    for url in followers_url:
        response = opener.open(url)
        html = response.read()
        followers.extend(re.findall(
            r'  <a href="/profile/(.+?)"><img src=', html))

    return followers


if __name__ == '__main__':
    # get_followers()
    init_url = 'http://www.programmableweb.com/category/all/apis'
    start_url = ["http://www.programmableweb.com/category/all/apis?page=%d" %
                 a for a in range(1, 528)]
    start_url.append(init_url)
    # print start_url
    for url in start_url:
        api_name = get_api_name(url)
        for name in api_name:
            followers, followers_num, opener = get_followers(name)
            if followers_num > 100:
                followers[len(followers):len(followers)] = get_followers_more(
                    name, followers_num, opener)
            try:
                file = open('.\\followers.txt', 'a')
                file.write(name + '\t' + '\t'.join(followers) + '\n')
            except Exception, e:
                pass
            finally:
                file.close()
