import json
import os
import scrapy
from scrapy.crawler import CrawlerProcess

from data_engineer_test import utils
from data_engineer_test.mongo import driver

class NewsSpider(scrapy.Spider):
    name = 'newsspider'
    start_urls = [
        'https://www.news.com.au/'
    ]

    def parse(self, response):
        for link in response.xpath('//div[contains(@class, "story-block")]/h4/a/@href').extract():
            yield response.follow(link, callback=self.parse_detail)
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath('//h1[contains(@class, "story-headline")]/text()').extract_first()
        author = response.xpath('//div[contains(@class, "author-info")]/text()').extract_first()
        content = response.xpath('//article/div[contains(@class, "story-content")]/'
                               'p/text()').extract()
        content_summary = response.xpath('//article/p[contains(@class, "description")]/text()').extract()

        yield {
            'title': utils.sanitise_string(title),
            'content': utils.sanitise_string(content),
            'content_summary': utils.sanitise_string(content_summary),
            'author' :  utils.sanitise_string(author),
            'url' : utils.sanitise_string(response.url)
        }

def main(event, context):
    #ensure the file exists on the lambda finction
    file = open("/tmp/result.json","w+")
    file.close()
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': '/tmp/result.json',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    })

    process.crawl(NewsSpider)
    process.start() # the script will block here until the crawling is finished

    with open('/tmp/result.json', 'rb') as myfile:
        data = myfile.read()

    python_collection = json.loads(data)

    mongo_driver = driver.MongoDriver()
    for j in python_collection:
        print(j)
        mongo_driver.insert_article(j)

    if os.path.exists("/tmp/result.json"):
        os.remove("/tmp/result.json")

    print('All done.')

#if __name__ == "__main__":
#    main('', '')

if __name__ == '__main__':
    #ensure the file exists on the lambda finction
    file = open("result.json","w+")
    file.close()

    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_URI': 'result.json',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    })

    process.crawl(NewsSpider)
    process.start() # the script will block here until the crawling is finished

    with open('result.json', 'rb') as myfile:
        data = myfile.read()

    python_collection = json.loads(data)

    mongo_driver = driver.MongoDriver()
    for j in python_collection:
        print(j)
        mongo_driver.insert_article(j)


    if os.path.exists("result.json"):
        os.remove("result.json")

    print("Success!")