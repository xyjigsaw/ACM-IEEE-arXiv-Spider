import scrapy
from scrapy.utils.project import get_project_settings
from acaSpider.items import AcaspiderItem
import logging
import re
import datetime
from acaSpider.proxyDownloader import getProxy


class ACMSpider(scrapy.Spider):
    name = "ACM_Spider"
    allowed_domains = ["dl.acm.org"]
    start_urls = get_project_settings().get('ACM_URL')

    def __init__(self):
        super(ACMSpider, self).__init__()
        self.startPage = 0
        self.pageSize = 20
        self.startTime = get_project_settings().get('START_TIME')
        getProxy().main()

    def parse(self, response):
        item = AcaspiderItem()
        print('爬取第', self.startPage, '页')
        results_num = response.xpath('//span[@class="hitsLength"]/text()').extract()[0].replace(',', '')
        item['title'] = list(map(self.remove_html, response.xpath('//span[@class="hlFld-Title"]/a/text()').extract()))
        item['authors'] = list(map(self.remove_html, response.xpath('//ul[@aria-label="authors"]').extract()))
        item['year'] = list(map(self.remove4year, list(map(self.remove_html, response.xpath('//span[@class="dot-separator"]').extract()))))
        item['typex'] = response.xpath('//span[@class="epub-section__title"]/text()').extract()
        item['subjects'] = response.xpath('//ul[@class="rlist--inline facet__list--applied"]/li/span/text()').extract()[0]  # 单值
        item['url'] = response.xpath('//a[@class="issue-item__doi dot-separator"]/text()').extract()
        item['abstract'] = list(map(self.remove_html, response.xpath('//div[@class="issue-item__abstract truncate-text trunc-done"]/p').extract()))
        item['citation'] = response.xpath('//span[@class="citation"]/span/text()').extract()  # 动态变化

        yield item
        logging.WARNING('已爬取：' + str((self.startPage + 1) * self.pageSize))

        if (datetime.datetime.now() - self.startTime).seconds > 3600:
            getProxy().main()
            print('已爬取：', (self.startPage + 1) * self.pageSize)
            logging.WARNING('$ ACM_Spider runs getProxy')

        if (self.startPage + 1) * self.pageSize < int(results_num) and self.startPage < 0:
            self.startPage += 1
            next_url = self.start_urls[0] + '&startPage=' + str(self.startPage) + '&pageSize=' + str(self.pageSize)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    def remove_html(self, string):
        pattern = re.compile(r'<[^>]+>')
        return (re.sub(pattern, '', string).replace('\n', '').replace('  ', '')).strip()

    def remove4year(self, string):
        return string.split(', ')[0]
