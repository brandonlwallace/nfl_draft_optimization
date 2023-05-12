# Run with:

# scrapy runspider mock_draft_scraper_part1.py  -O test_p1.csv 2> TRACE

from scrapy.spiders import Spider
from scrapy import Request


class MySpider(Spider):
    '''
    This class scrapes over the nflmockdraftdatabase site. It generates a dictionary
    and then populates it with the name of the outlet, the journalist, the timestamp, and
    the url portion upon click through. It uses the first 8 pages of the database.
    '''
    name = 'mockdraft'
    allowed_domains = ['nflmockdraftdatabase.com']
    start_urls = ['https://www.nflmockdraftdatabase.com/mock-drafts/2023',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/2',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/3',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/4',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/5',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/6',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/7',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/8']
    
    # setting up the parser
    def parse(self, response):
        # navigating to the table of results
        sites = response.xpath("//div[@class='mocks-list']//a[@class='site-link']")
        for site in sites:
            # setting an empty dictionary
            item = {}
            # filling the dictionary upon each loop with the corresponding xpath
            item['site_name'] = site.xpath('text()').get()
            item['author_name'] = site.xpath('../div[@class="extra-details"]//div[@class="site-author"]/text()').get()
            item['timestamp'] = site.xpath('../div[@class="extra-details"]//div[@class="site-timestamp"]/text()').get()
            item['url'] = site.xpath('@href').get()
            # printing to check that everything works
            print(item)
            yield item     

