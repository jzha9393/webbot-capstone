import fontTools.ttLib.woff2
import datetime
import scrapy
import pymysql


class AmazonSpider(scrapy.Spider):
    name = "AmazonSpider"
    domain = "https://www.amazon.com.au"
    start_urls = [
       "https://www.amazon.com.au/Nokia-2660-Flip-Feature-Phone/dp/B0B5WR623W?ref_=Oct_d_orec_d_4885143051_4&pd_rd_w=UM2Wx&content-id=amzn1.sym.fd0f28dc-0044-49ba-a22e-1d40da7cf07c&pf_rd_p=fd0f28dc-0044-49ba-a22e-1d40da7cf07c&pf_rd_r=92K8ETE0724ZR8495BBV&pd_rd_wg=YEwVK&pd_rd_r=06117f73-c92c-492a-a4df-364ac6fbdea6&pd_rd_i=B0B5WR623W&th=1"
    ]
    file = open('data.txt', 'a', encoding="utf-8")
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

    db = pymysql.connect(
            host = 'webbot.mysql.database.azure.com',
            user = 'admin111',
            password = 'webBot111',
            database = 'webbot'
        )

    cur = db.cursor()
    childDepartmentList = []

    def parse(self, response):
        return None

    def getModelNumber(self,response):
        listOfSpan = response.xpath("//th[contains(text(),'Item Model Number')]/parent::tr//td/text()")
        listOfSpan = listOfSpan.getall()
        if len(listOfSpan) == 1:
            return listOfSpan[0]
        return None

    def getProductDescription(self,response):
        listOfSpan = response.xpath("//ul[@class='a-unordered-list a-vertical a-spacing-mini']//li//span/text()")
        listOfSpan = listOfSpan.getall()
        result = ""
        for span in listOfSpan:
            result += span
            result += "\n"
        return result

    def getProductName(self,response):
        listOfSpan = response.xpath("//span[@id='productTitle']/text()")
        listOfSpan = listOfSpan.getall()
        if len(listOfSpan) == 1:
            return listOfSpan[0]
        return None

    def getProductBrand(self,response):
        listOfTr = response.xpath('//tr[@class="a-spacing-small po-brand"]//span/text()')
        listOfTr = listOfTr.getall()
        if len(listOfTr) == 2:
            return listOfTr[1]
        return None



    def parseDefault(self, response):
        url = response.url
        type = self.urlTypeCheck(url)
        if type == "department":
            list = self.getListOfChildDepartMent(response)
            if len(list) == 0:
                topProductList = self.getTopProductLinks(response)
                for link in topProductList:
                    link = response.urljoin(link)
                    yield scrapy.Request(url=link, callback=self.parse)
            else:
                for link in list:
                    link = response.urljoin(link)
                    yield scrapy.Request(url=link, callback=self.parse)
        elif type == "product":
            reviewlink = self.getReviewPage(response)
            reviewlink = response.urljoin(reviewlink)
            yield scrapy.Request(url=reviewlink, callback=self.parse)

        elif type == "reviews":
            self.getReviews(response)
    def getReviewPage(self,response):
        links = response.xpath('//a[contains(@data-hook,"see-all-reviews-link-foot")]/@href')
        links = links.getall()
        for link in links:

            return self.domain + link
    def getNextPage(self,response):
        links = response.xpath('//li[@class="a-last"]//a/@href')
        link = links.get()
        if link is None:
            return None
        link = self.domain + link

        return link

    def getReviews(self,response):
        listOfSpan = response.xpath('//span[contains(@data-hook,"review-body")]//span/text()')
        self.getNextPage(response)
        for span in listOfSpan.getall():
            self.file.write(span + "\n")
        """ nextPage = self.getNextPage(response)
        if nextPage is not None:
            url = response.urljoin(nextPage)
            yield scrapy.Request(url=url, callback=self.parse)"""
        titles = response.xpath('//a[contains(@data-hook,"review-title")]')
        dates = response.xpath('//span[contains(@data-hook,"review-date")]/text()')
        rantingDict = self.getRantingFromTitle(titles)
        for title in titles.getall():
            print(title)
            print("\n")
        dateList = self.australiaDateToSQLDate(dates.getall())
        titleList = self.getTitleTextFromTitleTag(titles)
        print(dateList)
        print("\n\n\n\n\n\n")
        print(rantingDict)

        i = 0
        for span in listOfSpan.getall():
            if i == 10:
                break
            sql = """ INSERT INTO amazonreviews.amazon_reviews (text, title, rating, date, platform)
                      VALUES(%s,%s,%s,%s,%s)
                  """
            tuple = (span,titleList[i],rantingDict["RantingList"][i],dateList[i],"Amazon")
            print(sql)
            i+=1
            self.cur.execute(sql,tuple)
            self.db.commit()

    def getListOfChildDepartMent(self,response):
        departments = response.xpath('//li[@class="a-spacing-micro apb-browse-refinements-indent-2"]//a/@href')
        list = departments.getall()
        return list

    def getTopProductLinks(self,response):
        links = response.xpath('//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href')
        links = links.getall()
        for link in links:
            return links


    def urlTypeCheck(self,url):
        if "/dp/" in url:
            return "product"
        if "/product-reviews/" in url:
            return "reviews"
        else:
            return "department"

    def getRantingFromTitle(self,titles):
        rantings = titles.xpath('//span[@class="a-icon-alt"]/text()')
        rantingDict = {}
        rantingList = rantings.getall()
        rantingDict["productRanting"] =float(rantingList[0][:3])
        reviewRanting = rantingList[3:13]
        intRantingList = []
        for review in reviewRanting:
            intRantingList.append(int(review[0]))
        rantingDict["RantingList"] = intRantingList
        return rantingDict

    def australiaDateToSQLDate(self,dates):
        listOfDate = []
        for date in dates:
            strList = (date.split(" "))
            pydate = datetime.date(int(strList[6]),self.monthStrToInt(strList[5]),int(strList[4]))
            listOfDate.append(pydate)
        return listOfDate

    def getTitleTextFromTitleTag(self,titles):
        listOfTitlesText = []
        listOfTitles = titles.xpath('//a[contains(@data-hook,"review-title")]//span[not(@class)]/text()')
        listOfTitlesText.extend(listOfTitles.getall())
        return listOfTitlesText[:10]

    def insertValueTables(self,texts,titles,dates,rating):
        i = 0
        resultList = []
        for text in texts:
            value = ()
    def monthStrToInt(self,str):
        return self.dateDict.get(str)

    def closed(self):
        self.file.close()

    def close(self):
        self.file.close()