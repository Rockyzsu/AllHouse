# coding: utf-8
import requests
import urllib
from lxml import etree
class CrawlHouse():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.headers = {"User-Agent": self.user_agent}


    def query(self,kw):

        url='https://shenzhen.anjuke.com/sale/rd1/?from=zjsr&kw=%E6%AC%A7%E9%99%86%E7%BB%8F%E5%85%B8'
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
    data=obj.query('ol')
    for x in data:
        print x[0],x[1]

if __name__=="__main__":
    main()