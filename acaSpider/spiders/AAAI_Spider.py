# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.project import get_project_settings
from acaSpider.items import AcaspiderItem
import logging
import re
import datetime
from acaSpider.proxyDownloader import getProxy

'''
    title = scrapy.Field()
    authors = scrapy.Field()
    year = scrapy.Field()
    typex = scrapy.Field()
    subjects = scrapy.Field()
    url = scrapy.Field()
    abstract = scrapy.Field()
    citation = scrapy.Field()
'''


class AAAISpider(scrapy.Spider):
    # for 2019-2010
    name = "AAAI_Spider"
    allowed_domains = ["aaai.org"]
    start_urls = get_project_settings().get('AAAI_URL')

    def __init__(self):
        super(AAAISpider, self).__init__()
        self.startTime = get_project_settings().get('START_TIME')
        self.proxyUpdateDelay = get_project_settings().get('PROXY_UPDATE_DELAY')
        getProxy().main()

    def parse(self, response):
        item = AcaspiderItem()

        item['title'] = list(map(self.remove_html, response.xpath('//p[@class="left"]/a[not(contains(text(), "PDF"))]').extract()))
        item['authors'] = response.xpath('//p[@class="left"]/i/text()').extract()
        if '19' in AAAISpider.start_urls[0]:
            item['year'] = (response.xpath('//div[@id="box6"]/p/text()').extract() * len(item['title']))[1::2]  # 存疑
        elif '18' in AAAISpider.start_urls[0]:
            item['year'] = ['New Orleans, Louisiana USA   —  February 2–7, 2018'] * len(item['title'])
        elif '17' in AAAISpider.start_urls[0]:
            item['year'] = ['February 4 –9, 2017, San Francisco, California USA'] * len(item['title'])
        elif '16' in AAAISpider.start_urls[0]:
            item['year'] = ['February 12 –17, 2016, Phoenix, Arizona USA'] * len(item['title'])
        elif '15' in AAAISpider.start_urls[0]:
            item['year'] = ['January 25 –30, 2015, Austin, Texas USA'] * len(item['title'])
        elif '14' in AAAISpider.start_urls[0]:
            item['year'] = ['July 27 –31, 2014, Québec City, Québec, Canada'] * len(item['title'])
        elif '13' in AAAISpider.start_urls[0]:
            item['year'] = ['July 14 –18, 2013, Bellevue, Washington, USA'] * len(item['title'])
        elif '12' in AAAISpider.start_urls[0]:
            item['year'] = ['July 22 –126, 2012, Toronto, Ontario, Canada'] * len(item['title'])
        elif '11' in AAAISpider.start_urls[0]:
            item['year'] = ['August 7 –11, 2011, San Francisco, California USA'] * len(item['title'])
        elif '10' in AAAISpider.start_urls[0]:
            item['year'] = ['July 11–15, 2010, Atlanta, Georgia'] * len(item['title'])
        elif '08' in AAAISpider.start_urls[0]:
            item['year'] = ['July 13–17, 2008, Chicago, Illinois'] * len(item['title'])
        item['typex'] = ['Association for the Advancement of Artificial Intelligence (AAAI)'] * len(item['title'])
        if '19' in AAAISpider.start_urls[0]:
            item['url'] = (response.xpath('//p[@class="left"]/a/@href').extract())[::2]
        else:
            item['url'] = (response.xpath('//p[@class="left"]/a/@href').extract())

        item['abstract'] = [' '] * len(item['title'])
        item['citation'] = [str(-1)] * len(item['title'])
        item['subjects'] = []
        raw_subjects = response.xpath('//p[@class="left"]/preceding-sibling::h4/text()').extract()  #
        tmp_subjects_cnt = []
        subjects_cnt = []
        for i in raw_subjects:
            tmp_subjects_cnt.append(self.get_subjects_cnt(response, i))
        for i in range(len(tmp_subjects_cnt) - 1):
            subjects_cnt.append(tmp_subjects_cnt[i + 1] - tmp_subjects_cnt[i])
        subjects_cnt.append(len(item['title']) - sum(subjects_cnt))
        if '17' in AAAISpider.start_urls[0]:
            subjects_cnt = [11, 26, 2, 1, 65, 25, 3, 3, 6, 33, 57, 182, 9, 11, 38, 18, 21, 16, 7, 14, 53, 16, 14, 8, 2, 17, 2, 9, 4, 1, 5, 7, 64, 16, 7, 13]
        elif '15' in AAAISpider.start_urls[0]:
            subjects_cnt = [59, 8, 2, 14, 20, 2, 44, 24, 8, 3, 10, 38, 43, 22, 8, 22, 16, 105, 30, 29, 5, 8, 18, 6, 13, 3, 20, 45, 16, 19, 6, 8]
        elif '11' in AAAISpider.start_urls[0]:
            subjects_cnt = [19, 6, 20, 48, 29, 14, 13, 14, 9, 7, 28, 18, 5, 10, 12, 19, 6, 44, 15, 8]
        for i in range(len(raw_subjects)):
            item['subjects'].extend(self.duplicate_subjects(raw_subjects[i], subjects_cnt[i]))
        if '13' in AAAISpider.start_urls[0]:
            item['title'] = item['title'][8:]
            item['authors'] = item['authors'][8:]
            item['year'] = item['year'][8:]
            item['typex'] = item['typex'][8:]
            item['url'] = item['url'][8:]
            item['abstract'] = item['abstract'][8:]
            item['citation'] = item['citation'][8:]
        print(raw_subjects)
        print(tmp_subjects_cnt)
        print(subjects_cnt)
        yield item

    def get_subjects_cnt(self, response, subject):
        return len(response.xpath('//div[@class="content"]//h4[contains(text(), "' + subject + '")]/preceding-sibling::p').extract())

    def duplicate_subjects(self, string, num):
        return [string] * num

    def remove_html(self, string):
        pattern = re.compile(r'<[^>]+>')
        return (re.sub(pattern, '', string).replace('\n', '').replace('  ', '')).strip()
