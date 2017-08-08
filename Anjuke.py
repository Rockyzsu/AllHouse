# coding: utf-8
import Queue

import requests
import urllib
from lxml import etree
import  xlwt
class CrawlHouse():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.headers = {"User-Agent": self.user_agent}


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

    #简单版本 耗时短
    def getAllCommunity(self,NextPage,q):

        s=requests.get(url=NextPage,headers=self.headers)
        print s.status_code
        tree=etree.HTML(s.text)

        #getEach:
        all_list=tree.xpath('//div[@_soj="xqlb"]')
        for each in all_list:
            name= each.xpath('.//a[@hidefocus="true"]/@title')[0]
            print name
            address=each.xpath('.//address/text()')[0].strip()
            print address

            build_data=each.xpath('.//p[@class="date"]/text()')[0].strip()
            print build_data
            price=each.xpath('.//strong/text()')[0]
            print price


            detailPage_lnk = each.xpath('.//a[@hidefocus="true"]/@href')[0]

            print "Detail link", detailPage_lnk

            s = requests.get(url='https://shenzhen.anjuke.com'+detailPage_lnk, headers=self.headers, timeout=5)
            # print s.text
            t2 = etree.HTML(s.text)
            basic_info = t2.xpath('//dl[@class="basic-parms-mod"]')[0]
            wuye_type = basic_info.xpath('.//dt/text()')
            dict_k = []
            dict_v = []

            for x in wuye_type:
                print x
                dict_k.append(x)
            wuye_detail = basic_info.xpath('.//dd/text()')
            for x in wuye_detail:
                print x
                dict_v.append(x)

            detail_dict = zip(dict_k, dict_v)
            print detail_dict

            data= [name,address,build_data,price]

            q.put(data)

        nextPage=tree.xpath('//a[@class="aNxt"]/@href')
        if len(nextPage)!=0:
            nextPageLnk=nextPage[0]
            print nextPageLnk
            #self.getAllCommunity(nextPageLnk,q)

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



if __name__=="__main__":
    main()