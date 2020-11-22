import scrapy
from scrapy.crawler import CrawlerProcess


class GutenbergSpider(scrapy.Spider):
    name = 'gutenberg'
    allowed_domains = ['projekt-gutenberg.org']

    start_urls = ['https://www.projekt-gutenberg.org/autoren/info/autor-az.html']
    #author_base_url = 'https://www.projekt-gutenberg.org/autoren/'

    def parse(self, response):
        author_links = response.xpath("//body/table[@class='center']//a/@href")
        for href in author_links:
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_author_page)

    def parse_author_page(self, response):
        name = response.xpath("//h2[@class='name']/text()").extract_first()
        print(name)
        
        archived = response.xpath("//div[@class='archived']//li")

        for doc in archived:
            title = doc.xpath(".//a/text()").extract_first()
            url = response.urljoin(doc.xpath(".//a/@href").extract_first())
            
            if len(title) > 0:
                yield {'name': name, 'title': title, 'url': url}
        
            
def runCrawler(name):
    c = CrawlerProcess({
        'CLOSESPIDER_PAGECOUNT': 20,
        'USER_AGENT': 'HochschuleDarmstadt-TextWebMining',
        'FEED_FORMAT': 'csv',
        'FEED_URI': '/media/sf_Shared/Git/data/GutenbergSpider.csv',
        'DOWNLOAD_DELAY': 1,
        'ROBOTSTXT_OBEY': True,
        'HTTPCACHE_ENABLED': True

    })
    c.crawl(eval(name))
    c.start() # the script will block here until the crawling is finished

runCrawler('GutenbergSpider')
