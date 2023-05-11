# -*- coding: utf-8 -*-
"""
Scraper for Mock Draft Data

@author: Brandon Wallace

"""

# Run with:

# python -m scrapy runspider mock_draft_scraper.py -O mock_data.csv 2> TRACE

# Scraper for main page and each mock draft 

from scrapy.spiders import Spider
from scrapy import Request


class MySpider(Spider):
    '''
    This class runs on https://www.nflmockdraftdatabase.com/. The spider extracts the ****
    
    '''

#TBD