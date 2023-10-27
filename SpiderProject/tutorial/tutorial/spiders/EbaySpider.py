import fontTools.ttLib.woff2
import datetime
import scrapy
import pymysql


class AmazonSpider(scrapy.Spider):
    name = "EbaySpider"
    domain = "https://www.ebay.com.au/"
    start_urls = [
       "https://www.ebay.com.au/b/Bean-Bag-Toys/49019/bn_1843407"
    ]
    file = open('data2.txt', 'a', encoding="utf-8")
    dateDict = {
            "January" : 1,
            "February" : 2,
            "March" : 3,
            "April" : 4,
            "May" : 5,
            "June" : 6,
            "July" : 7,
            "August" :8,
            "September" : 9,
            "October"  : 10,
            "November" : 11,
            "December" : 12
        }

    db = pymysql.connect(host='localhost',
                         user='root',
                         password='hjkk445998',
                         database='notepile')

    cur = db.cursor()
    childDepartmentList = []

    def parse(self, response):
        departments = response.xpath('//div[@class="b-tile__img"]/parent::*/parent::*/@href')
        list = departments.getall()
        for department in list:
            print(department)
            print("\n")
            self.file.writelines(list)

    def getUrlFromBestSelling(self,response):
        departments = response.xpath('//div[@class="b-tile__img"]/parent::*/parent::*/@href')
        list = departments.getall()
        for department in list:
            print(department)
            print("\n")
            self.file.writelines(list)

    def getSubCatagoryInSeeALLPage(self,response):
        departments = response.xpath('//section[@class="b-module b-list b-categorynavigations b-display--landscape"]'
                                     '/ul//li/a/@href')
        list = departments.getall()
        for department in list:
            print(department)
            print("\n")
            self.file.writelines(list)


    def getAllURLWithoutSeeALL(self,response):
        departments = response.xpath('//section[@class="b-module b-list b-categorynavigations b-display--landscape"]'
                                     '/ul/li[not(ul)]')
        list = departments.getall()
        for department in list:
            print(department)
            print("\n")
            self.file.writelines(list)

    def getAllSeeAllURL(self,response):
        departments = response.xpath(
            '//section[@class="b-module b-list b-categorynavigations b-display--landscape"]//'
            'ul[@class="b-accordion-subtree"]//li//a[contains(text(),"See")]/@href')
        list = departments.getall()
        for department in list:
            print(department)
            print("\n")
            self.file.writelines(list)

    def closed(self):
        self.file.close()

    def close(self):
        self.file.close()