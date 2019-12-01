import scrapy
import re
from scrapy import Request


class ToScrapePlayerStats(scrapy.Spider):
    name = 'scrape_players_url'
    start_urls = [
        'https://sofifa.com/players?offset=0'
    ]

    # Function to scrape the url for every every player and putting it in a file.
    def parse(self, response):
        f = open('../out/players_url_list.out', 'a')
        link_dict = {}
        for player in response.xpath('.'):
            footballers_list = response.xpath('.//a[@class="nowrap"]/@href').extract()
            for footballer in footballers_list:
                f.write(response.urljoin(footballer) + '\n')

        next_page = response.xpath('.//div[@class="pagination"]/a[last()]/@href').get()
        if next_page:
            yield Request(response.urljoin(next_page))

