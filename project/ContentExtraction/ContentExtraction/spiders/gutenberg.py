import scrapy
from scrapy.crawler import CrawlerProcess


class GutenbergSpider(scrapy.Spider):
    name = 'gutenberg'
    allowed_domains = ['projekt-gutenberg.org']

    start_urls = ['https://www.projekt-gutenberg.org/info/texte/the-gesc.html']
    #author_base_url = 'https://www.projekt-gutenberg.org/autoren/'

    def parse(self, response):
        items = response.xpath("//body//dl/dd")
        for item in items:
            author = item.xpath("./text()").extract_first().strip()
            a_tag = item.xpath("./a")
            if a_tag:
                title = a_tag.xpath("./text()").extract_first()
                url = response.urljoin(a_tag.xpath("./@href").extract_first())
                #print(author, title, url)
                yield scrapy.Request(url, callback = self.parse_document_page, meta={'author': author, 'title': title})

    def parse_document_page(self, response):
        p_tags = response.xpath("//*/p[count(preceding-sibling::hr)=1]")
        
        text = ""
        for p_tag in p_tags:
            paragraph = p_tag.xpath("./text()").extract_first().strip()
            text += paragraph + '\n'
        
        yield {'author': response.meta.get('author'), 'title': response.meta.get('title'), 'chapter': text.strip()}
        
        
            
def runCrawler(name):
    c = CrawlerProcess({
        'CLOSESPIDER_PAGECOUNT': 10,
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
