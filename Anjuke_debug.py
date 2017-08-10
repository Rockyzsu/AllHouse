# coding: utf-8
import Queue
import random
import chardet
import requests
import urllib
import sqlite3
from lxml import etree
import xlwt
import codecs
from pandas import Series, DataFrame

q = Queue.Queue()


class CrawlHouse():
    def __init__(self):
        self.my_userAgent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)']

        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        cookie_read = open('cookie').read().strip()
        self.headers = {"user-agent": self.user_agent, 'cookie': cookie_read}

    def query(self, city, kw):
        # kw=欧陆经典
        kw = urllib.quote(kw)

        # url='https://shenzhen.anjuke.com/sale/rd1/?from=zjsr&kw=%s' %kw
        url = 'https://%s.anjuke.com/sale/rd1/?from=zjsr&kw=%s' % (city, kw)
        s = requests.get(url=url, headers=self.headers, timeout=5)
        print s.status_code
        tree = etree.HTML(s.text)
        # title=tree.xpath('//a')
        t1 = tree.xpath('//div[@class="search-lessresult div-border"]')[0]
        # print t1
        price = t1.xpath('.//em[@class="price"]/text()')[0]
        print price
        detailPage_lnk = t1.xpath('.//a[@class="comm-detail "]/@href')[0]
        s = requests.get(url=detailPage_lnk, headers=self.headers, timeout=5)
        # print s.text
        t2 = etree.HTML(s.text)
        basic_info = t2.xpath('//dl[@class="basic-parms-mod"]')[0]
        wuye_type = basic_info.xpath('.//dt/text()')
        dict_k = []
        dict_v = []
        dict_k.append(u'小区名字:   ')
        dict_v.append(kw)
        dict_k.append(u'均价:  ')
        dict_v.append(price)
        for x in wuye_type:
            # print x
            dict_k.append(x)
        wuye_detail = basic_info.xpath('.//dd/text()')
        for x in wuye_detail:
            # print x
            dict_v.append(x)

        detail_dict = zip(dict_k, dict_v)
        print detail_dict

        # 物业类型
        # 总建面积
        # 建造年代
        # 容积率
        # 开发商
        # 物业公司
        return detail_dict

    # 获取某个城市的所有小区  简单信息
    def getAllCommunity_simple(self, cityLink, NextPage, f):
        # user_agent = random.choice(self.my_userAgent)
        # headers = {'User-Agent': user_agent}
        NextUrl = cityLink + NextPage
        s = requests.get(url=NextUrl, headers=self.headers)
        print s.status_code
        tree = etree.HTML(s.text)
        # getEach:
        all_list = tree.xpath('//div[@_soj="xqlb"]')

        for each in all_list:

            name = each.xpath('.//a[@hidefocus="true"]/@title')[0]
            print name
            address = each.xpath('.//address/text()')[0].strip()
            print address
            f.write(name)
            f.write('\t')
            build_data = each.xpath('.//p[@class="date"]/text()')[0].strip()
            print build_data
            try:
                price = each.xpath('.//strong/text()')[0]
                print price
            except Exception, e:
                return
            f.write(price)
            f.write('\t')
            f.write(address)
            f.write('\t')
            f.write(build_data)
            f.write('\n')

        nextPage = tree.xpath('//a[@class="aNxt"]/@href')
        if len(nextPage) != 0:
            nextPageLnk = nextPage[0]
            print nextPageLnk
            nextPageNum = nextPageLnk.split(cityLink)[1]
            self.getAllCommunity_simple(cityLink, nextPageNum, f)

    # waste
    def getPageDetail(self):
        url = 'https://shenzhen.anjuke.com/sale/?kw=%E6%AC%A7%E9%99%86%E7%BB%8F%E5%85%B8&from=xlts_mc&k_comm_id=95393'
        s = requests.get(url=url, headers=self.headers)
        print s.status_code
        # print s.text
        tree = etree.HTML(s.text)
        link = tree.xpath('//a[@class="comm-detail "]/@href')
        # print link
        if len(link) != 0:
            lnk = link[0]
            print lnk
            s = requests.get(url=lnk, headers=self.headers)
            tree_page = etree.HTML(s.text)

    # 得到所有城市
    def getCity(self):
        url = 'https://www.anjuke.com/sy-city.html'
        s = requests.get(url=url, headers=self.headers)
        tree = etree.HTML(s.text)
        node = tree.xpath('//div[@class="city_list"]')
        result = []
        for i in node:
            x = i.xpath('.//a/text()')
            y = i.xpath('.//a/@href')
            for a in range(len(x)):
                print x[a], y[a]
                result.append([x[a], y[a]])
                # y[a] link
        return result

    # 获取所有小区
    def getAllCityCommunity(self):
        all_city = self.getCity()
        for i in all_city:
            print "Getting city ", i[0]
            self.f = codecs.open(i[0] + '.txt', 'a', encoding='utf-8')
            self.getAllCommunity(i[1], '/community/p1/', self.f)
            self.f.close()

    def saveCity(self):
        data = self.getCity()
        with codecs.open('city_list.txt', 'a', encoding='utf-8') as f:
            for i in data:
                f.write(i[0])
                f.write('\t')
                f.write(i[1])
                f.write('\n')


def main():
    obj = CrawlHouse()
    # obj.getPageDetail()
    '''
    data=obj.query('shenzhen','万科四季花城(一期)')
    for x in data:
        print x[0],x[1]
    '''
    q = Queue.Queue()
    obj.getAllCommunity('https://shenzhen.anjuke.com/community/p1/', q)
    print "Done"
    final_data = []
    while not q.empty():
        final_data.append(q.get())


def testcase():
    obj = CrawlHouse()
    # obj.saveCity()
    # q = Queue.Queue()
    obj.getAllCityCommunity()
    # obj.getAllCommunity('https://shenzhen.anjuke.com/community/p1/')
    # print "Done"
    '''
    final_data=[]
    while not q.empty():
        final_data.append(q.get())

    for i in final_data:
        for x in i:
            print x[0],x[1]
    '''

if __name__ == "__main__":
    # main()
    testcase()
