# coding: utf-8
import Queue
import random
import chardet
import requests
import urllib
import sqlite3
from lxml import etree
import  xlwt
import codecs
from pandas import Series,DataFrame
q=Queue.Queue()
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
        cookie_read=open('cookie').read().strip()
        self.headers = {"user-agent": self.user_agent,'cookie':cookie_read}

    #获取某个城市的所有小区  简单信息
    def getAllCommunity_simple(self,cityLink,NextPage, f):
        #user_agent = random.choice(self.my_userAgent)
        #headers = {'User-Agent': user_agent}
        NextUrl=cityLink+NextPage
        s=requests.get(url=NextUrl,headers=self.headers,timeout=5)
        print s.status_code
        tree=etree.HTML(s.text)

        #getEach:

        all_list=tree.xpath('//div[@_soj="xqlb"]')

        for each in all_list:

            dict_k = [ ]
            dict_v = [ ]
            name= each.xpath('.//a[@hidefocus="true"]/@title')[0]
            print name
            #address=each.xpath('.//address/text()')[0].strip()
            #print address
            f.write(name)
            f.write('\t')
            #build_data=each.xpath('.//p[@class="date"]/text()')[0].strip()
            #print build_data
            try:
                price=each.xpath('.//strong/text()')[0]
                print price
            except Exception,e:
                return
            f.write(price)
            f.write('\t')
            dict_k.append(u'名字')
            dict_v.append(name)
            #print type(dict_k)
            dict_k.append(u'均价')
            dict_v.append(price)

            detailPage_lnk = each.xpath('.//a[@hidefocus="true"]/@href')[0]

            print "Detail link", detailPage_lnk

            #user_agent = random.choice(self.my_userAgent)
            #headers = {'User-Agent': user_agent}
            s = requests.get(url=cityLink+detailPage_lnk, headers=self.headers, timeout=5)
            # print s.text
            t2 = etree.HTML(s.text)
            basic_info = t2.xpath('//dl[@class="basic-parms-mod"]')[0]
            wuye_type = basic_info.xpath('.//dt/text()')


            for x in wuye_type:
                #print unicode(x)
                #print type(x)
                #print chardet.detect(x)
                dict_k.append(x.encode('utf-8'))
            wuye_detail = basic_info.xpath('.//dd/text()')
            for x in wuye_detail:
                #print unicode(x)
                #print type(x)
                #print chardet.detect(x)
                f.write(x)
                f.write('\t')


                dict_v.append(x.encode('utf-8'))

            detail_dict = zip(dict_k, dict_v)
            print detail_dict
            #df=DataFrame(dict(detail_dict),index=[0])
            #data= [name,address,build_data,price]
            #df.to_csv('data.csv',mode='a')
            q.put(detail_dict)
            f.write('\n')

        nextPage=tree.xpath('//a[@class="aNxt"]/@href')
        if len(nextPage)!=0:
            nextPageLnk=nextPage[0]
            print nextPageLnk
            nextPageNum=nextPageLnk.split(cityLink)[1]
            self.getAllCommunity(cityLink,nextPageNum,f)

            # 获取某个城市的所有小区 详细信息
    #def getAllCommunity(self, cityLink, NextPage, f):
    def getAllCommunity(self, cityLink, NextPage, f):
                # user_agent = random.choice(self.my_userAgent)
                # headers = {'User-Agent': user_agent}
                NextUrl = cityLink + NextPage
                s = requests.get(url=NextUrl, headers=self.headers, timeout=5)
                print s.status_code
                tree = etree.HTML(s.text)

                # getEach:

                all_list = tree.xpath('//li[@class="clear xiaoquListItem"]')

                for each in all_list:

                    dict_k = []
                    dict_v = []
                    name = each.xpath('.//div/@class="title"/a/text()')[0]
                    print name
                    # address=each.xpath('.//address/text()')[0].strip()
                    # print address
                    #f.write(name)
                    #f.write('\t')
                    # build_data=each.xpath('.//p[@class="date"]/text()')[0].strip()
                    # print build_data
                    '''
                    try:
                        price = each.xpath('.//strong/text()')[0]
                        print price
                    except Exception, e:
                        return
                    f.write(price)
                    f.write('\t')
                    dict_k.append(u'名字')
                    dict_v.append(name)
                    # print type(dict_k)
                    dict_k.append(u'均价')
                    dict_v.append(price)

                    detailPage_lnk = each.xpath('.//a[@hidefocus="true"]/@href')[0]

                    print "Detail link", detailPage_lnk

                    # user_agent = random.choice(self.my_userAgent)
                    # headers = {'User-Agent': user_agent}
                    s = requests.get(url=cityLink + detailPage_lnk, headers=self.headers, timeout=5)
                    # print s.text
                    t2 = etree.HTML(s.text)
                    basic_info = t2.xpath('//dl[@class="basic-parms-mod"]')[0]
                    wuye_type = basic_info.xpath('.//dt/text()')

                    for x in wuye_type:
                        # print unicode(x)
                        # print type(x)
                        # print chardet.detect(x)
                        dict_k.append(x.encode('utf-8'))
                    wuye_detail = basic_info.xpath('.//dd/text()')
                    for x in wuye_detail:
                        # print unicode(x)
                        # print type(x)
                        # print chardet.detect(x)
                        f.write(x)
                        f.write('\t')

                        dict_v.append(x.encode('utf-8'))
                    '''
                    '''
                    detail_dict = zip(dict_k, dict_v)
                    print detail_dict
                    # df=DataFrame(dict(detail_dict),index=[0])
                    # data= [name,address,build_data,price]
                    # df.to_csv('data.csv',mode='a')
                    q.put(detail_dict)
                    f.write('\n')

                nextPage = tree.xpath('//a[@class="aNxt"]/@href')
                if len(nextPage) != 0:
                    nextPageLnk = nextPage[0]
                    print nextPageLnk
                    nextPageNum = nextPageLnk.split(cityLink)[1]
                    self.getAllCommunity(cityLink, nextPageNum, f)
                '''
        #得到所有城市
    def getCity(self):
        url='https://www.anjuke.com/sy-city.html'
        s=requests.get(url=url,headers=self.headers)
        tree=etree.HTML(s.text)
        node=tree.xpath('//div[@class="city_list"]')
        result=[]
        for i in node:
            x= i.xpath('.//a/text()')
            y= i.xpath('.//a/@href')
            for a in range(len(x)):
                print x[a],y[a]
                result.append([x[a],y[a]])
            #y[a] link
        return result

    #获取所有小区
    def getAllCityCommunity(self):
        #all_city=self.getCity()
        with open('city_list.txt','r') as fp:
            all_list=fp.readlines()
            print all_list
            all_city=map(lambda x:x.split('\t'),all_list)
            #print all_city

        for i in all_city:
            print "Getting city ", i[0],i[1]
            self.f = codecs.open(i[0].decode('utf-8')+'.txt', 'a', encoding='utf-8')
            self.getAllCommunity(i[1].strip(),'/community/p1/', self.f)
            self.f.close()

    def saveCity(self):
        data=self.getCity()
        with codecs.open('city_list.txt','a',encoding='utf-8') as f:
            for i in data:
                f.write(i[0])
                f.write('\t')
                f.write(i[1])
                f.write('\n')


def main():
    obj=CrawlHouse()
    f=''
    obj.getAllCommunity('https://sz.lianjia.com','/ershoufang/pg2/',f)




if __name__=="__main__":
    main()
    #testcase()