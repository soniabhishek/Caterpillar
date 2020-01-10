import scrapy
from competitors.crunchcom.items import CrunchComItem


class CompetitorsSpider(scrapy.Spider):
    name = "competitors"
    companies = {}

    def __init__(self, company, **kwargs):
        self.start_urls = [f'https://www.crunchbase.com/organization/{company}']
        self.companies[f'/organization/{company}'] = company
        super().__init__(**kwargs)  # python3

    def parse(self, response):
        competitors_elem = response.css(
            "[cbtableofcontentsitem='Competitors & Revenue by Owler'] list-markup-block .cb-link")
        unique_compnaies = {}
        for elem in competitors_elem:
            link = elem.attrib['href']
            if link not in self.companies:
                self.companies[link] = elem.attrib['title']
                unique_compnaies[link] = elem.attrib['title']

        for link, company in unique_compnaies.items():
            c_item = CrunchComItem()
            c_item['business_name'] = company
            c_item['url'] = link
            yield c_item
            yield response.follow(link, self.parse)

        return self.companies
