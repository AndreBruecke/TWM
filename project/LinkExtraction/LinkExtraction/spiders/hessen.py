import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor


class HessenSpider(scrapy.Spider):
    name = 'hessen'
    allowed_domains = ['hessen.de']
    start_urls = ['https://www.hessen.de/']

    def parse(self, response):
        if ("www.hessen.de" in response.url):
            extractor = LinkExtractor(allow_domains='hessen.de') #, deny=("veranstaltungskalender", "jcalpro"))
            #extractor = LinkExtractor()  # , deny=("veranstaltungskalender", "jcalpro"))
            links = extractor.extract_links(response)
            extractor = LinkExtractor(deny_domains=('hessen.de', 'facebook.com', 'youtube.com', 'twitter.com', 'instagram.com', 'radroutenplaner.hessen.de'))
            linksext = extractor.extract_links(response)
            for link in linksext:
                yield {'from': response.url, 'url': link.url, 'text': link.text.strip()}
            for link in links:
                absolute_next_page_url = response.urljoin(link.url)
                yield scrapy.Request(absolute_next_page_url)

c = CrawlerProcess({
    'USER_AGENT': 'HochschuleDarmstadt-TextWebMining',
    'FEED_FORMAT': 'csv',
    'FEED_URI': '/media/sf_Shared/Git/data/HessenSpider.csv',
    'DOWNLOAD_DELAY' : 1,
    'ROBOTSTXT_OBEY' : True,
    'HTTPCACHE_ENABLED' : True
})


c.crawl(HessenSpider)
c.start() # the script will block here until the crawling is finished