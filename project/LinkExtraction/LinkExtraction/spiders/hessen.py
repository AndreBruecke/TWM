import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor


class HessenSpider(scrapy.Spider):
    name = 'hessen'
    allowed_domains = ['hessen.de']
    start_urls = ['https://www.hessen.de/regierung/']

    def parse(self, response):
        if ("www.hessen.de" in response.url):
            extractor = LinkExtractor(allow='regierung', allow_domains='hessen.de')
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
    'FEED_URI': '/media/sf_Shared/Git/data/HessenRegierung.csv',
    'DOWNLOAD_DELAY' : 1,
    'ROBOTSTXT_OBEY' : True,
    'HTTPCACHE_ENABLED' : True
})


c.crawl(HessenSpider)
c.start() # the script will block here until the crawling is finished
