# coding: utf-8
import requests
from lxml import etree
#Q房
class CrawlHouse():
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        self.headers = {"User-Agent": self.user_agent}

    def getData(self,location):
        #url2='http://shenzhen.qfang.com/sale/futian'
        url='http://shenzhen.qfang.com'+location
        s=requests.get(url,headers=self.headers)
        print s.status_code
        tree=etree.HTML( s.text)

        #获取需要的数据
        page_house=tree.xpath('//div[@class="show-detail"]')
        for i in page_house:
            title=i.xpath('.//p/a/@title')[0]
            year=i.xpath('./')

            print "小区名字", name


        #nextPage=tree.css('a.turnpage_next::attr(href)').extarct_first()
        nextPage=tree.xpath('//a[@class="turnpage_next"]/@href')
        if len(nextPage)!=0:
            print nextPage[0]
            #self.getData(nextPage[0])


def main():
    obj=CrawlHouse()
    obj.getData('/sale/nanshan/f1')

if __name__=='__main__':
    main()