import scrapy
from demoFullUnitop.items import DemofullunitopItem

class FullunitopSpider(scrapy.Spider):
    name = "FullUnitop"
    allowed_domains = ["unitop.vn"]
    start_urls = ["https://unitop.vn/"]
    def parse_start(self):
        yield scrapy.Request(url = start_urls, callback = self.parse)

    def parse(self, response):
        cousrseList = response.xpath('//div[@class="box-body"]/ul/li/div/a/@href').getall()
        for courseItem in cousrseList:
            item = DemofullunitopItem()
            item['courseURL'] = response.urljoin(courseItem)
            request = scrapy.Request(url = response.urljoin(courseItem), callback = self.parseCourseDetail)
            request.meta['datacourse'] = item
            yield request
    
    def parseCourseDetail(self, response):
        item = response.meta['datacourse']
        item['title'] = response.xpath('normalize-space(//h1[@class="course-title"]/text())').get() 
        item['description'] = response.xpath('normalize-space(//p[@class="course-desc"]/text())').get() 
        item['vote'] = response.xpath('normalize-space(//span[@class="num-vote"]/text())').get() 
        item['total'] = response.xpath('normalize-space(//div[@class="total_student"]/text())').get() 
        item['mentor'] = response.xpath('normalize-space(//a[@class="mentor"]/text())').get()
        yield item
