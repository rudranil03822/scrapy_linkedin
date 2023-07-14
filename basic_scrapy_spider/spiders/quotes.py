

import json
import scrapy

class LinkedCompanySpider(scrapy.Spider):
    name = "linkedin_company_profile"

    #add your own list of company urls here
    company_pages = [
        'https://www.linkedin.com/company/event-engage'
        ]


    def start_requests(self):
        
        company_index_tracker = 0

        first_url = self.company_pages[company_index_tracker]

        yield scrapy.Request(url=first_url, callback=self.parse_response, meta={'company_index_tracker': company_index_tracker})


    def parse_response(self, response):
        company_index_tracker = response.meta['company_index_tracker']
        print('***************')
        print('****** Scraping page ' + str(company_index_tracker+1) + ' of ' + str(len(self.company_pages)))
        print('***************')

        company_item = {}

        # company_item['name'] = response.css('.top-card-layout__entity-info h1::text').get(default='not-found').strip()
        # company_item['summary'] = response.css('.top-card-layout__entity-info h4 span::text').get(default='not-found').strip()
        all_text = response.css('::text').getall()
        company_item['all_text'] = ' '.join(all_text).strip().replace('\n','')

        try:
            ## all company details 
            company_details = response.css('.core-section-container__content .mb-2')

            #industry line
            company_industry_line = company_details[1].css('.text-md::text').getall()
            company_item['industry'] = company_industry_line[1].strip()

            #company size line
            company_size_line = company_details[2].css('.text-md::text').getall()
            company_item['size'] = company_size_line[1].strip()

            #company founded
            company_size_line = company_details[5].css('.text-md::text').getall()
            company_item['founded'] = company_size_line[1].strip()

            # Save company_item as JSON
            self.save_as_json(company_item)
        except IndexError:
            print("Error: Skipped Company - Some details missing")

        yield company_item
        

        company_index_tracker = company_index_tracker + 1

        if company_index_tracker <= (len(self.company_pages)-1):
            next_url = self.company_pages[company_index_tracker]

            yield scrapy.Request(url=next_url, callback=self.parse_response, meta={'company_index_tracker': company_index_tracker})
    

    def save_as_json(self, data):
        filename = 'company_data.json'
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        self.log(f'Saved data as JSON: {filename}')

    def readUrlFromFile(self):
        self.company_pages = []
        