# -*- coding: utf-8 -*-
"""
Scraper for Mock Draft Data

@author: Brandon Wallace

"""

# Run with:

# python -m scrapy runspider mock_draft_scraper.py > TRACE

# Scraper for main page and each mock draft 

from scrapy.spiders import Spider
from scrapy import Request
import csv


class MySpider(Spider):
    '''
    This class scrapes the individual pages of each mock draft obtained from
    the main page of the site. It takes the name of each player in the order 
    that they are picked in the mock draft and writes the picks to a CSV file. 
    Each row in the CSV file represents a separate mock draft.
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
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/8',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/9',
                  'https://www.nflmockdraftdatabase.com/mock-drafts/2023/page/10']
    base = 'https://www.nflmockdraftdatabase.com/'
    
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,
        # Download delay increased to 1.0 seconds to prevent throttling
        'DOWNLOADER_CLIENT_TLS_METHOD' : 'TLSv1.2',
        'USER_AGENT' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36(KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
        }

    def parse(self, response):
        # Navigate to the table of results
        sites = response.xpath("//div[@class='mocks-list']//a[@class='site-link']")
        for site in sites:
            # Get the url of the mock draft page
            url = site.xpath('@href').get()
            # Make a request to the mock draft page
            yield Request(self.base + url, callback=self.parse_mock_draft)
    
    
    def parse_mock_draft(self, response):
        # Extract all player names from the page
        player_names = response.xpath("//div[@class='player-name player-name-bold']//text()")
        # Set up the CSV writer
        output_file = "mock_draft_data.csv"  
        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["site_name", "author_name", "timestamp"] + ["pick{}".format(i) for i in range(1, len(player_names)+1)])

            # Write the site metadata and each player name to a separate column in the CSV file
            row = {}
            row["site_name"] = response.xpath("//h1//text()").extract()
            row["author_name"] = response.xpath("//div[@class='page-author-name']//span//text()").extract()
            row["timestamp"] = response.xpath("//time//text()").extract()
            for i, player_name in enumerate(player_names, start=1):
                row["pick{}".format(i)] = player_name.get().strip()
            writer.writerow(row)
            # Check that everything is working with print statement
            print(f"Row data: {row}")
            writer.writerow(row)
    












