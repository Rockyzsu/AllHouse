# coding: utf-8
import Queue
import random
import re

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

        self.headers = {"user-agent": self.user_agent}
        #self.headers = {"user-agent": self.user_agent,'cookie':cookie_read}

    def query(self,city,kw):
        #kw=欧陆经典
        kw=urllib.quote(kw)

        #url='https://shenzhen.anjuke.com/sale/rd1/?from=zjsr&kw=%s' %kw
        url='https://%s.anjuke.com/sale/rd1/?from=zjsr&kw=%s' %(city,kw)
        s=requests.get(url=url,headers=self.headers,timeout=5)
        print s.status_code
        tree=etree.HTML(s.text )
        #title=tree.xpath('//a')
        t1=tree.xpath('//div[@class="search-lessresult div-border"]')[0]
        #print t1
        price=t1.xpath('.//em[@class="price"]/text()')[0]
        print price
        detailPage_lnk=t1.xpath('.//a[@class="comm-detail "]/@href')[0]
        s = requests.get(url=detailPage_lnk, headers=self.headers,timeout=5)
        #print s.text
        t2=etree.HTML(s.text)
        basic_info=t2.xpath('//dl[@class="basic-parms-mod"]')[0]
        wuye_type=basic_info.xpath('.//dt/text()')
        dict_k=[]
        dict_v=[]
        dict_k.append(u'小区名字:   ')
        dict_v.append(kw)
        dict_k.append(u'均价:  ')
        dict_v.append(price)
        for x in wuye_type:
            #print x
            dict_k.append(x)
        wuye_detail=basic_info.xpath('.//dd/text()')
        for x in wuye_detail:
            #print x
            dict_v.append(x)

        detail_dict=zip(dict_k,dict_v)
        print detail_dict

        #物业类型
        #总建面积
        #建造年代
        #容积率
        #开发商
        #物业公司
        return detail_dict

    #获取某个城市的所有小区  简单信息
    def getAllCommunity_simple(self,cityLink,NextPage, f,proxies):
        #user_agent = random.choice(self.my_userAgent)
        #headers = {'User-Agent': user_agent}
        NextUrl=cityLink+NextPage
        s=requests.get(url=NextUrl,headers=self.headers,timeout=5)
        print s.status_code
        p=re.compile(u'请输入图片中的验证码')
        if p.findall(s.text):
            print "需要手动输入验证码"
            raw_input("打开浏览器，输入验证码后按Enter确认键继续")

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
            p = re.compile(u'请输入图片中的验证码')
            if p.findall(s.text):
                print "需要手动输入验证码"
                raw_input("打开浏览器，输入验证码后按Enter确认键继续")
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
    def getAllCommunity(self, cityLink, NextPage, f,proxies):
                # user_agent = random.choice(self.my_userAgent)
                # headers = {'User-Agent': user_agent}
                NextUrl = cityLink + NextPage
                s = requests.get(url=NextUrl, headers=self.headers, timeout=15,proxies=proxies)
                p = re.compile(u'请输入图片中的验证码')
                if p.findall(s.text):
                    print "需要手动输入验证码"
                    raw_input("打开浏览器，输入验证码后按Enter确认键继续")
                    s = requests.get(url=NextUrl, headers=self.headers, timeout=15,proxies=proxies)
                print s.status_code
                tree = etree.HTML(s.text)

                # getEach:

                all_list = tree.xpath('//div[@_soj="xqlb"]')

                for each in all_list:

                    dict_k = []
                    dict_v = []
                    name = each.xpath('.//a[@hidefocus="true"]/@title')[0]
                    print name
                    # address=each.xpath('.//address/text()')[0].strip()
                    # print address
                    f.write(name)
                    f.write('\t')
                    # build_data=each.xpath('.//p[@class="date"]/text()')[0].strip()
                    # print build_data
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
                    try:
                        s = requests.get(url=cityLink + detailPage_lnk, headers=self.headers, timeout=15,proxies=proxies)
                    except Exception,e:
                        print e
                        return
                    # print s.text
                    p = re.compile(u'请输入图片中的验证码')
                    if p.findall(s.text):
                        print "需要手动输入验证码"
                        raw_input("打开浏览器，输入验证码后按Enter确认键继续")
                        s = requests.get(url=cityLink + detailPage_lnk, headers=self.headers, timeout=15,proxies=proxies)
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
                    self.getAllCommunity(cityLink, nextPageNum, f,proxies)

    #waste
    def getPageDetail(self):
        url='https://shenzhen.anjuke.com/sale/?kw=%E6%AC%A7%E9%99%86%E7%BB%8F%E5%85%B8&from=xlts_mc&k_comm_id=95393'
        s=requests.get(url=url,headers=self.headers)
        print s.status_code
        #print s.text
        tree=etree.HTML(s.text)
        link=tree.xpath('//a[@class="comm-detail "]/@href')
        #print link
        if len(link)!=0:
            lnk=link[0]
            print lnk
            s=requests.get(url=lnk,headers=self.headers)
            tree_page=etree.HTML(s.text)
    #异常处理
    def ExceptionHandle(self):
        url='https://shenzhen.anjuke.com/community/p1/'
        session=requests.session()
        proxies={
            'http':'http://114.217.241.162:8118'
        }

        s=session.get(url=url,headers=self.headers)
        #r=requests.get(url=url,headers=self.headers)
        print s.cookies
        #print s.status_code
        print s.text
        p=re.compile(u'请输入图片中的验证码')
        if p.findall(s.text):
            print "需要手动输入验证码"

        num=int(round(random.random() * 1000))
        url='https://www.anjuke.com/v3/ajax/captcha/newimage?id='+str(num)
        s=session.get(url=url,headers=self.headers)
        #切换cookie
        with open('captha.png','wb') as f:
            f.write(s.content)





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
        #proxies={'http':'http://122.72.32.73:80'}
        proxies={'http': '180.105.126.75:8118'}
        for i in all_city:
            print "Getting city ", i[0],i[1]
            self.f = codecs.open(i[0].decode('utf-8')+'.txt', 'a', encoding='utf-8')
            self.getAllCommunity(i[1].strip(),'/community/p1/', self.f,proxies)
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
    #obj.getPageDetail()
    '''
    data=obj.query('shenzhen','万科四季花城(一期)')
    for x in data:
        print x[0],x[1]
    '''
    q=Queue.Queue()
    obj.getAllCommunity('https://shenzhen.anjuke.com/community/p1/',q)
    print "Done"
    final_data=[]
    while not q.empty():
        final_data.append(q.get())

def testcase():
    obj=CrawlHouse()
    #obj.saveCity()
    #q = Queue.Queue()
    obj.getAllCityCommunity()
    #obj.getAllCommunity('https://shenzhen.anjuke.com/community/p1/')
    #print "Done"
    #obj.saveCity()
    #obj.ExceptionHandle()
    '''
    final_data=[]
    while not q.empty():
        final_data.append(q.get())

    for i in final_data:
        for x in i:
            print x[0],x[1]
    '''
if __name__=="__main__":
    #main()
    testcase()