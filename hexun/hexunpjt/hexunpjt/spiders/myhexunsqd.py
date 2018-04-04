# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from hexunpjt.items import HexunpjtItem
import time
import urllib
import re

class MyhexunsqdSpider(scrapy.Spider):
    name = 'myhexunsqd'
    allowed_domains = ['hexun.com']
    uid="19940007"
    def start_requests(self):
        yield Request("http://"+str(self.uid)+".blog.hexun.com/p1/default.html",headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})
    # Request(url,callback,headers={});对于start_requests 中的Request则不需要指定callback 其默认的callback是 parse
    # start_urls = []

    def parse(self, response):
        items=[]
        num = len(response.xpath("//span[@class='ArticleTitleText']/a/text()"))
        num2= len(response.xpath('//div[@class="PageSkip_1"]/a'))
        page = int(response.xpath('//div[@class="PageSkip_1"]/a/text()').extract()[num2-2])
        pat1 = '<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        # hcurl为存储评论数和点击数的网址，为一个javascript程序
        hcurl = re.compile(pat1).findall(str(response.body))[0]
        # 模拟成浏览器头部
        headers2 = ("User-Agent",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
        opener = urllib.request.build_opener()
        opener.addheaders = [headers2]
        # 将opener安装为全局
        urllib.request.install_opener(opener)
        # data为通过浏览器打开JavaScript的数据
        data = urllib.request.urlopen(hcurl).read()
        # pat2为提取文章阅读数的正则表达式
        pat2 = "click\d*?','(\d*?)'"
        # pat3为提取文章评论数的正则表达式
        pat3 = "comment\d*?','(\d*?)'"
        # 提取阅读数和评论数数据并分别赋值给列表list_hit和list_com
        list_hit = re.compile(pat2).findall(str(data))
        list_com = re.compile(pat3).findall(str(data))
       #思路还是采用锚点的方式先找到锚点，然后逐个item进行赋值 ；如果锚点不明确，则可以使用下面的方式直接利用XPATH绝对路径来查找
        for i in range(num):
            item=HexunpjtItem()
            item["name"]=response.xpath("//span[@class='ArticleTitleText']/a/text()").extract()[i]
            item["url"]= response.xpath("//span[@class='ArticleTitleText']/a/@href").extract()[i]
            item["hit"]=list_hit[i]
            item["comment"]=list_com[i]
            item["byte"] = response.xpath("//span[@class='ArticleWordCount']/text()").extract()[i]
            #直接yield item返回 item，然后再继续执行，充分利用 twist的异步执行特性，牛逼之处 ！
            yield item
        for i in range(2, page):
            # 构造下一次要爬取的url，爬取一下页博文列表页中的数据
            nexturl = "http://" + str(self.uid) + ".blog.hexun.com/p" + str(i) + "/default.html"
            # 进行下一次爬取，下一次爬取仍然模拟成浏览器进行
            yield Request(nexturl, callback=self.parse, headers={
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0"})

