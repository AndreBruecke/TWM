import scrapy
from scrapy.crawler import CrawlerProcess


class GutenbergSpider(scrapy.Spider):
    name = 'gutenberg'
    allowed_domains = ['projekt-gutenberg.org']

    genre_names = {
        'https://www.projekt-gutenberg.org/info/texte/the-gesc.html': 'Geschichte',
        'https://www.projekt-gutenberg.org/info/texte/the-phil.html': 'Philosophie und Religion',
        'https://www.projekt-gutenberg.org/info/texte/the-kult.html': 'Kultur und Kunst',
        'https://www.projekt-gutenberg.org/info/texte/the-nat.html': 'Natur, Wissen und Reise',
        'https://www.projekt-gutenberg.org/info/texte/the-bio.html': 'Biographie'
    }

    start_urls = genre_names.keys()
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
                yield scrapy.Request(url, callback = self.parse_document_page, meta={'author': author, 'title': title, 'genre': self.genre_names[response.request.url]})

    def parse_document_page(self, response):
        p_tags = response.xpath("//body/h3/following-sibling::p")
        
        text = ""
        for p_tag in p_tags:
            paragraph = p_tag.xpath("./text()").extract_first()
            if paragraph:
                text += paragraph.strip() + '\n'
        
        if len(text) > 1000:
            yield {'author': response.meta.get('author'), 'title': response.meta.get('title'), 'genre': response.meta.get('genre'), 'chapter': text.strip()}
        else:
            rel_url = response.xpath("//body/a[starts-with(text(), 'weiter')]/@href").extract_first()
            if not rel_url:
                rel_url = response.xpath("//body/a[starts-with(@href, 'chap')]/@href").extract_first()
            
            if rel_url:
                url = response.urljoin(rel_url)
                yield scrapy.Request(url, callback=self.parse_document_page, meta=response.meta)
            else:
                yield {'author': response.meta.get('author'), 'title': response.meta.get('title'), 'genre': response.meta.get('genre'), 'chapter': text.strip()}
        
        
            
def runCrawler(name):
    c = CrawlerProcess({
        'USER_AGENT': 'HochschuleDarmstadt-TextWebMining',
        'FEED_FORMAT': 'csv',
        'FEED_URI': '/media/sf_Shared/Git/data/GutenbergGenres.csv',
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': True,
        'HTTPCACHE_ENABLED': True

    })
    c.crawl(eval(name))
    c.start() # the script will block here until the crawling is finished

runCrawler('GutenbergSpider')
