import scrapy
import json
import sys
sys.path.append('jobs_ai/spiders/utils') #my machine...
sys.path.append('utils')
import utils
import os
from utils import JobItem

APPLYTO_JOB_URLS = os.path.join(os.path.dirname(__file__),'applytojob_job_urls.json')

class ApplytojobSpider(scrapy.Spider):

    name = "applytojob"
    allowed_domains = ["applytojob.com"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25 # seconds
    }

    def __init__(self, name=None, **kwargs):      
        self.start_urls = [f"https://{url['url']}" 
            for url 
            in json.load(open(APPLYTO_JOB_URLS))]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
    

    def parse(self, response):
        job_links = response.xpath("//li[contains(@class,'list-group-item')]/h4/a/@href")
       
        for job_link in job_links:
            href = job_link.extract()
            yield scrapy.Request(href, callback=self.parse_thread, dont_filter=True, meta={'url': href})

    def parse_thread(self, response):
        url = response.meta.get('url')
        company = json.loads(response.xpath('/html/head/script[2]/text()')[0].extract())
        workplace_types = response.css('div.posting-category.workplaceTypes::text').get()
        try:
            logo = response.xpath("//div[@class='brand-logo']//img/@src")[0].extract().strip(),
        except:
            logo=''
    
        job = JobItem(
            company_name = company['name'].strip(),
            job_title = response.xpath("//div[@class='job-header']//h1/text()")[0].extract().strip(),
            description =  utils.clean_html(response.xpath("//div[@id='job-description']")[0].extract()),
            city = response.xpath("//div[@title='Location']/text()")[1].extract().strip(),
            job_type = [
                response.xpath("//div[@id='resumator-job-employment']/text()")[1].extract().strip()
            ],
            location_type=[
                
            ],
            date_posted= "",
            company_link= company['url'],
            company_logo= logo,
            job_board= company['name'],
            application_link= url,
            salary = utils.get_salary(response.xpath("//div[@id='job-description']")[0].extract()),
        )
        yield job
       
       
        
        
       
