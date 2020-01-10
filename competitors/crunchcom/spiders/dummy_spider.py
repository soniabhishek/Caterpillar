import scrapy
from competitors.crunchcom.items import CrunchComItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CompetitorsSpider(CrawlSpider):
    name = "dummy"
    companies = {}
    rules = (
        Rule(LinkExtractor(allow=('organization/',), restrict_css=("[cbtableofcontentsitem='Competitors & Revenue by Owler'] list-markup-block .cb-link")), callback='parse_it', follow=True),
    )

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
    }

    def __init__(self, company, **kwargs):
        self.start_urls = [f'https://www.crunchbase.com/organization/{company}']
        self.companies[f'/organization/{company}'] = company
        super().__init__(**kwargs)  # python3

    def parse_it(self, response):
        print(response)
