import scrapy
from acaSpider.items import AcaspiderItem
from scrapy.utils.project import get_project_settings


class IEEESpider(scrapy.Spider):
    name = "IEEE_Spider"
    allowed_domains = ["ieeexplore.ieee.org"]
    start_urls = get_project_settings().get('IEEE_URL')

    def parse(self, response):
        # Developing in progress
        item = AcaspiderItem()
        item['title'] = response.xpath('//a').extract()
        print('%%%%%%%%%%--', item['title'])
        item['authors'] = response.xpath('//p[@class="author"]/text()').extract()[0]
        item['year'] = response.xpath('//h1[@class="title-article"]/text()').extract()[0]
        item['type'] = response.xpath('//h1[@class="title-article"]/text()').extract()[0]
        item['publisher'] = response.xpath('//h1[@class="title-article"]/text()').extract()[0]

