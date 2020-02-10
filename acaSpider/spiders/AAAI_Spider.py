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
    # for 2019
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
        item['year'] = (response.xpath('//div[@id="box6"]/p/text()').extract() * len(item['title']))[1::2]  # 存疑
        item['typex'] = ['Association for the Advancement of Artificial Intelligence (AAAI)'] * len(item['title'])
        item['url'] = (response.xpath('//p[@class="left"]/a/@href').extract())[::2]  #
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
        for i in range(len(raw_subjects)):
            item['subjects'].extend(self.duplicate_subjects(raw_subjects[i], subjects_cnt[i]))

        yield item

    def get_subjects_cnt(self, response, subject):
        return len(response.xpath('//div[@class="content"]//h4[contains(text(), "' + subject + '")]/preceding-sibling::p').extract())

    def duplicate_subjects(self, string, num):
        return [string] * num

    def remove_html(self, string):
        pattern = re.compile(r'<[^>]+>')
        return (re.sub(pattern, '', string).replace('\n', '').replace('  ', '')).strip()
