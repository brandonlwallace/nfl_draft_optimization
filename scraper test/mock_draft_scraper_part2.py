# Run with:

# scrapy runspider mock_draft_scraper_part2.py  -O test_p2.csv 2> TRACE

import csv
from scrapy.spiders import Spider
from scrapy import Request


class MySpider(Spider):
    '''
    This class takes the name of each player in the order that they are picked in the mock draft. 
    In order to keep the picks seperate, it processes the picks as new columns where each 
    player is on the same row 
    '''
    name = 'sports-gambling-mock'
    allowed_domains = ['nflmockdraftdatabase.com']
    start_urls = ['https://www.nflmockdraftdatabase.com/mock-drafts/2023/sports-gambling-podcast-2023-sean-green?date=2023-04-24']
    
    # setting up the parser
    def parse(self, response):
        # Extract all player names from the page
        player_names = response.xpath("//div[@class='player-name player-name-bold']//text()")

        # Set up the CSV writer
        output_file = "test_p2.csv"
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["pick{}".format(i) for i in range(1, len(player_names)+1)])
            writer.writeheader()

            # Write each player name to a separate column in the CSV file
            row = {}
            for i, player_name in enumerate(player_names, start=1):
                row["pick{}".format(i)] = player_name.get().strip()
            writer.writerow(row)
    
    
