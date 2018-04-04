# -*- coding: utf-8 -*-
import pymysql
import time
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HexunpjtPipeline(object):
    # def __init__(self):
    #     self.conn=pymysql.connect(host="127.0.0.1",user="root",passwd="root",db="hexun")
    def process_item(self, item, spider):
        conn = pymysql.connect(host="127.0.0.1", user="root", passwd="root", db="hexun",charset="utf8")
        cur=conn.cursor()
        name=item['name']
        url=item['url']
        hit=item['hit']
        comment=item['comment']
        byte=item['byte']

        cur.execute("INSERT INTO myhexun(name,url,hit,comment,byte) VALUES(%s,%s,%s,%s,%s)",(name,url,hit,comment,byte))

        conn.commit()
        conn.close()
     #  time.sleep(1)
        return item
