import scrapy
from ..items import FarascraperItem

class FaraSpider(scrapy.Spider):
    name = "fara"
    start_urls = ['https://efile.fara.gov/ords/f?p=1381:1:1880917662158:::::']

    def parse(self, response):
        LIST_SELECTOR = '#L305833146647729924'
        
        for pageTable in response.css(LIST_SELECTOR):

            LINK_SELECTOR = 'li a::attr(href)'
            url = response.urljoin(pageTable.css(LINK_SELECTOR).get())
            yield scrapy.Request(url,callback=self.parse_table_contents)

    def parse_table_contents(self,response):
        items = FarascraperItem()

        TABLE_SELECTOR ='tr'

        for tableContent in response.css(TABLE_SELECTOR):
            LINK_SELECTOR = 'tr td a::attr(href)'
            FP_SELECTOR = 'td:nth-child(2) ::text'
            ADDRESS_SELECTOR = 'td:nth-child(4) ::text'
            STATE_SELECTOR = 'td:nth-child(5) ::text'
            REGISTRANT_SELECTOR = 'td:nth-child(6) ::text'
            REG_NUM_SELECTOR = '.u-tC ::text'
            REG_DATE_SELECTOR = '.u-tC+ .u-tL ::text'

            url = tableContent.css(LINK_SELECTOR).get()
            if url is not None:
                if url != "#":
                    items['url'] = url
                else:
                    continue
            else:
                continue
            
            items['state'] = tableContent.css(STATE_SELECTOR).get()
            items['reg_num'] = tableContent.css(REG_NUM_SELECTOR).get()
            items['address'] = tableContent.css(ADDRESS_SELECTOR).get()
            items['foreign_principal'] = tableContent.css(FP_SELECTOR).get()
            items['date'] = tableContent.css(REG_DATE_SELECTOR).get()
            items['registrant'] = tableContent.css(REG_NUM_SELECTOR).get()
            items['exhibit_url'] = 'PDF FILE'

            yield items

            # yield {
            #     'URL': 'https://efile.fara.gov/ords/'+ str(tableContent.css(LINK_SELECTOR).get()),
            #     'Foreign Principal': tableContent.css(FP_SELECTOR).get(),
            #     # 'FP Registration Date': tableContent.css(FP_REG_DATE_SELECTOR).get(),
            #     'ADDRESS': tableContent.css(ADDRESS_SELECTOR).get(),
            #     'STATE': tableContent.css(STATE_SELECTOR).get(),
            #     'REGISTRANT': tableContent.css(REGISTRANT_SELECTOR).get(),
            #     'REGISTRATION #': tableContent.css(REG_NUM_SELECTOR).get(),
            #     'REGISTRATION DATE': tableContent.css(REG_DATE_SELECTOR).get(),
            #     # 'Country': tableContent.xpath(COUNTRY_SELECTOR).get(),
            # }
