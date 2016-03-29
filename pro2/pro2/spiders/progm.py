# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.http import Request
from pro2.items import programmable, followers, mushup
# import time
# from selenium import webdriver
# import json
# import re


class ProgmSpider(scrapy.Spider):
    name = "progm"
    allowed_domains = ["programmableweb.com"]
    url = 'http://www.programmableweb.com/category/all/apis'

    # http://www.programmableweb.com/category/all/apis?page=1
    url1 = 'http://www.programmableweb.com/category/all/apis?search_id=147085&deadpool=1'
    # http://www.programmableweb.com/category/all/apis?page=142&search_id=147085&deadpool=1
    start_url = ["http://www.programmableweb.com/category/all/apis?page=%d&search_id=147085&deadpool=1" %
                 a for a in range(1, 144)]
    start_url.append(url1)
    start_urls = start_url

    def parse(self, response):

        for sel in response.xpath('//td[@class="views-field views-field-title col-md-3"]/a/@href').extract():
            url = 'http://www.programmableweb.com' + sel
            # print url
            yield Request(url, callback=self.parse2)

    def parse2(self, response):
        item = programmable()
        item['API_Name'] = response.xpath(
            """//*[@class="node-header"]/h1/text()""").extract()

        item['API_ID'] = response.xpath(
            """//li[@class="last leaf pull-left text-uppercase"]/a/@href""").extract()[0].split('/')[-1]

        item['Description'] = response.xpath(
            """//div[@class="api_description tabs-header_description"]/text()""").extract()[0].strip()
        item['Primary_Category'] = []
        item['Secondary_Categories'] = []
        item['API_Homepage']=[]
        # 部分网页的格式是不一样的 遍历所有的div元素来找出所要的信息
        for sel in response.xpath('//div[@class="section specs"]/div[@class="field"]'):
            if sel.xpath('label/text()').extract()[0] == 'Secondary Categories':
                item['Secondary_Categories'] = sel.xpath(
                    'span/a/text()').extract()
            if sel.xpath('label/text()').extract()[0] == 'Primary Category':
                item['Primary_Category'] = sel.xpath(
                    'span/a/text()').extract()
            if sel.xpath('label/text()').extract()[0]=='API Homepage':
                item['API_Homepage']=sel.xpath('span/a/text()').extract()
            if sel.xpath('label/text()').extract()[0]=='API Provider':
                item['API_Provider']=sel.xpath('span/a/text()').extract()

        item['Followers_Number'] = response.xpath(
            """//section[@id="block-views-api-followers-row-top"]/div[1]/span/text()""").extract()

        # 示例网址：http://www.programmableweb.com/api/quova/followers
        yield item

        url2 = response.url + '/followers'
        yield Request(url2, callback=self.parse3)
        # musghups
        # //*[@id='block-views-api-mashups-new-list-top']/div[2]/div[1]/a
        url3 = "http://www.programmableweb.com" + \
            response.xpath(
                "//*[@id='block-views-api-mashups-new-list-top']/div[2]/div[1]/a/@href").extract()[0]
        yield Request(url3, callback=self.parse4)

    def parse3(self, response):
        # 如果follows数量超过一百，在一页上显示不全 最多100个
        item = followers()
        # //*[@id='followers']/div[2]/div[2]/table/tbody/tr[1]/td[2]/a
        # //*[@id='followers']/div[2]/div[2]/table/tbody/tr[2]/td[2]/a
        # //*[@id='followers']/div[2]/div[2]/table/tbody/tr[17]/td[2]/a
        # //*[@id='followers']/div[2]/div[2]/table/tbody/tr[1]/td[2]/a
        item['API_ID'] = response.xpath(
            '//li[@class="last leaf pull-left text-uppercase"]/a/@href').extract()[0].split('/')[-2]
        item['Followers_Name'] = []
        for sel in response.xpath("//*[@id='followers']/div[2]/div[2]/table/tbody/tr/td[2]/a"):
            temp = sel.xpath('text()').extract()[0]
            item['Followers_Name'].append(temp)
        yield item

    def parse4(self, response):
        # //*[@id='block-system-main']/article/div[7]/div[1]/table/tbody/tr[1]/td[1]/a
        # //*[@id='block-system-main']/article/div[7]/div[1]/table/tbody/tr[2]/td[1]/a
        # //*[@id='block-system-main']/article/div[7]/div[1]/table/tbody/tr[1]/td[1]/a
        item = mushup()
        item['API_ID'] = response.url.split('=')[-1]
        item['mushup_name'] = []
        for sel in response.xpath("//*[@id='block-system-main']/article/div[7]/div[1]/table/tbody/tr/td[1]/a"):
            temp = sel.xpath('text()').extract()[0]
            item['mushup_name'].append(temp)
        yield item
