import requests
from lxml import etree
import os


class getProxy:
    def __init__(self):
        self.url = 'http://www.xicidaili.com/'
        self.headers = self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.path = 'proxy_list.txt'

    def getHtml(self):
        res = requests.get(self.url, headers=self.headers)
        res.encoding = 'utf-8'
        html = res.text
        self.parseHtml(html)

    def parseHtml(self, html):
        lst = []
        # 构建xpath解析对象
        parsehtml = etree.HTML(html)
        # 获取IP元素对象
        iplist = parsehtml.xpath('//tr/td[2]')
        # 获取port元素对象
        portlist = parsehtml.xpath('//tr/td[3]')
        # 获取地区元素对象
        addrlist = parsehtml.xpath('//tr/td[4]')
        # 获取是否高匿对象
        iflist = parsehtml.xpath('//tr/td[5]')
        # 获取代理协议类型对象
        typelist = parsehtml.xpath('//tr/td[6]')
        # 写入本地
        num = 0
        for x, y, z, m, n in zip(iplist, portlist, addrlist, iflist, typelist):
            if x.text and y.text and z.text and m.text and n.text:
                if 's' not in n.text and 'S' not in n.text:
                    write_text = n.text + '://' + x.text + ':' + y.text + '\n'
                    self.writeComment(write_text)
                    num += 1
        print('共采集代理：', num)

    def writeComment(self, lst):
         with open(self.path, 'a') as f:
             f.write(lst)

    # 主函数
    def main(self):
        if os.path.exists(self.path):
            os.remove(self.path)
        self.getHtml()


if __name__ == '__main__':
    xici = getProxy()
    xici.main()

