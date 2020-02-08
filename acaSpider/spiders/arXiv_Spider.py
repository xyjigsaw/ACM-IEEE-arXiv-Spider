import scrapy
from acaSpider.items import AcaspiderItem
from scrapy.utils.project import get_project_settings
from lxml import etree
from typing import *
from acaSpider.proxyDownloader import getProxy
import logging


class arXivSpider(scrapy.Spider):
    name = 'arXiv_Spider'
    allowed_domains = ['export.arxiv.org']
    start_urls = get_project_settings().get('ARXIV_URL')

    def __init__(self):
        super(arXivSpider, self).__init__()
        self.startTime = get_project_settings().get('START_TIME')
        self.startItem = 0
        self.pageSize = 2
        self.retryTime = 5  # optional
        self.categorySet = Category()  # Static
        self.category = self.get_next_category()  # num++
        self.urlFromSetting = get_project_settings().get('ARXIV_URL')[0]
        self.next_url = self.urlFromSetting.format(CAT=self.category, START=self.startItem, MAX=self.pageSize)
        arXivSpider.start_urls[0] = self.next_url

        self.debugTime = 2  # need removing

    def get_next_category(self):
        return self.categorySet.CS.get_value(list(self.categorySet.CS.subCategory)[self.categorySet.CS.categoryNum])

    def parse(self, response):
        item = AcaspiderItem()
        response = etree.HTML(bytes(bytearray(response.text.replace('arxiv:', 'arxiv').replace('\n', ''), encoding='utf-8')))
        item['title'] = response.xpath('//entry/title/text()')
        item['year'] = response.xpath('//entry/published/text()')
        item['abstract'] = list(map(self.strip_blank, response.xpath('//entry/summary/text()')))
        item['url'] = response.xpath('//entry/id/text()')
        multi_response = response.xpath('//feed//entry')
        item['authors'] = []
        item['subjects'] = []
        item['typex'] = []
        item['citation'] = []
        for res in multi_response:
            item['authors'].append(','.join(res.xpath('.//author/name/text()')))
            item['subjects'].append(','.join(res.xpath('.//category/@term')))
            item['typex'].append(''.join(self.replace_NULL(res.xpath('.//arxivjournal_ref/text()'))))
            item['citation'].append(str(-1))

        yield item
        item_cnt = len(item['title'])
        logging.warning('$ arXiv_Spider已爬完一页：' + self.category + ', 数量：'+str(self.startItem + item_cnt))

        if (item_cnt == self.pageSize) and self.debugTime:
            self.debugTime -= 1

            self.startItem += self.pageSize
            self.next_url = self.urlFromSetting.format(CAT=self.category, START=self.startItem, MAX=self.pageSize)
            self.retryTime = 3
            yield scrapy.Request(url=self.next_url, callback=self.parse)
            print(self.next_url)
        elif item_cnt == 0 and self.retryTime:
            self.retryTime -= 1
            yield scrapy.Request(url=self.next_url, callback=self.parse)
        else:
            logging.warning('$ arXiv_Spider已爬完某一小类：' + self.category + ' 总数：' + str(self.startItem + item_cnt))
            try:
                self.category = self.get_next_category()
                self.startItem = 0
                self.retryTime = 3
                self.next_url = self.urlFromSetting.format(CAT=self.category, START=self.startItem, MAX=self.pageSize)
                yield scrapy.Request(url=self.next_url, callback=self.parse, dont_filter=True)
            except IndexError:
                logging.warning('$ arXiv_Spider已爬完某一大类')

    def replace_NULL(self, info):
        if not info:
            info = 'arXiv'
        return info

    def replace_ABBR(self, string):
        pass

    def strip_blank(self, string):
        return string.strip()


class SubCategory(object):
    '''保持子类别的常数'''

    def __init__(self, category_name: str, sub_category: Dict[str, str]):
        self.categoryName = category_name
        self.subCategory = sub_category
        self.categoryNum = 0

    def get_value(self, value):
            if value in list(self.subCategory):
                self.categoryNum += 1
                return self.subCategory[value]
            else:
                raise Exception('No value name:', value)


class Category(object):

    CS = SubCategory('cs',
                     {'AI': 'Artificial Intelligence',
                      'CC': 'Computational Complexity',
                      'CG': 'Computational Geometry',
                      'CE': 'Computational Engineering, Finance, and Science',
                      'CL': 'Computation and Language (Computational Linguistics and Natural Language and Speech Processing)',
                      'CV': 'Computer Vision and Pattern Recognition',
                      'CY': 'Computers and Society',
                      'CR': 'Cryptography and Security',
                      'DB': 'Databases',
                      'DS': 'Data Structures and Algorithms',
                      'DL': 'Digital Libraries',
                      'DM': 'Discrete Mathematics',
                      'DC': 'Distributed, Parallel, and Cluster Computing',
                      'ET': 'Emerging Technologies',
                      'FL': 'Formal Languages and Automata Theory',
                      'GT': 'Computer Science and Game Theory',
                      'GL': 'General Literature',
                      'GR': 'Graphics',
                      'AR': 'Hardware Architecture',
                      'HC': 'Human-Computer Interaction',
                      'IR': 'Information Retrieval',
                      'IT': 'Information Theory',
                      'LG': 'Machine Learning',
                      'LO': 'Logic in Computer Science',
                      'MS': 'Mathematical Software',
                      'MA': 'Multiagent Systems',
                      'MM': 'Multimedia',
                      'NI': 'Networking and Internet Architecture',
                      'NE': 'Neural and Evolutionary Computation',
                      'NA': 'Numerical Analysis',
                      'OS': 'Operating Systems',
                      'OH': 'Other',
                      'PF': 'Performance',
                      'PL': 'Programming Languages',
                      'RO': 'Robotics',
                      'SI': 'Social and Information Networks',
                      'SE': 'Software Engineering',
                      'SD': 'Sound',
                      'SC': 'Symbolic Computation',
                      'SY': 'Systems and Control',
                      }
                     )



