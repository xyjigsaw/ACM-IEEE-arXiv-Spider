# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import pymysql
from twisted.enterprise import adbapi


class AcaspiderPipeline(object):
    def process_item(self, item, spider):
        for title, authors, year, typex, url, abstract, citation in zip(item['title'], item['authors'], item['year'],
                                                                        item['typex'], item['url'], item['abstract'],
                                                                        item['citation']):
            print('========================')
            print('标题：', title)
            print('作者：', authors)
            print('年份：', year)
            print('期刊/会议：', typex)
            print('主题：', item['subjects'])
            print('URL：', url)
            print('摘要：', abstract)
            print('引用：', citation)
            print('========================')

            txt_str = '\n========================' + '\n标题：' + title + '\n作者：' + authors + '\n年份：' + year + \
                      '\n期刊/会议：' + typex + '\n主题：' + item['subjects'] + '\nURL：' + url + '\n摘要：' + abstract + \
                      '\n引用：' + citation + '\n========================'
            self.write2txt(txt_str)

            json_str = {'title': title, 'authors': authors, 'year': year, 'type': typex, 'subjects': item['subjects'],
                        'URL': url, 'abstract': abstract, 'citation': citation}
            self.write2json(json_str)
        return item

    def write2txt(self, txt_str):
        with open('ACMSpider_info.txt', 'a') as f:
            f.write(txt_str)

    def write2json(self, json_str):
        with open('ACM_Spider_Data.json', 'a') as json_file:
            json_file.write(json.dumps(json_str) + '\n')


class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        # 连接数据池ConnectionPool，使用pymysql连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
        insert into ACM_Data(title,authors,year,type,subjects,url,abstract,citation) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    """

        for title, authors, year, typex, url, abstract, citation in zip(item['title'], item['authors'],
                                                                        item['year'],
                                                                        item['typex'], item['url'],
                                                                        item['abstract'],
                                                                        item['citation']):

            cursor.execute(insert_sql, (title, authors, year, typex, item['subjects'], url, abstract, citation))

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)
            logging.error('$ messages from MysqlPipeline: ' + str(failure))

