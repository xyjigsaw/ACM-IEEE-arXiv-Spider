import scrapy
import re
from acaSpider.items import AcaspiderItem
from scrapy.utils.project import get_project_settings


class arXivSpider(scrapy.Spider):
    name = "arXiv_Spider"
    allowed_domains = ["arxiv.org"]
    start_urls = get_project_settings().get('ARXIV_URL')

    def parse(self, response):
        # Developing in progress

        # get num line
        num = response.xpath('//*[@id="dlpage"]/small[1]/text()[1]').extract()[0]
        # get max_index
        max_index = int(re.search(r'\d+', num).group(0))
        for index in range(1, max_index + 1):
            item = AcaspiderItem()
            # get title and clean data
            title = response.xpath('//*[@id="dlpage"]/dl/dd[' + str(index) + ']/div/div[1]/text()').extract()
            # remove blank char
            title = [i.strip() for i in title]
            # remove blank str
            title = [i for i in title if i is not '']
            # insert title
            try:
                item['title'] = title[0]
            except IndexError:

                item['title'] = 'error'
            authors = ''
            # authors'  father node
            xpath_fa = '//*[@id="dlpage"]/dl/dd[' + str(index) + ']/div/div[2]//a/text()'
            author_list = response.xpath(xpath_fa).getall()
            authors = str.join('', author_list)
            item['authors'] = authors

            item['subjects'] = response.xpath(
                'string(//*[@id="dlpage"]/dl/dd[' + str(5) + ']/div/div[5]/span[2])').extract_first()

            yield item
        # 这里下一个url指向的是1802，改为循环就可以爬取全部信息
        # yield scrapy.Request('https://arxiv.org/list/cs.CV/1802?show=1000', callback=self.parse)


