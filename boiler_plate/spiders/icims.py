import scrapy
import json
import sys
import os
sys.path.append('jobs_ai/spiders/utils') #my machine...
sys.path.append('utils')
import utils
from utils import JobItem

ICIMS_JOB_URLS = os.path.join(os.path.dirname(__file__),'icims_job_urls.json')

class IcimsSpider(scrapy.Spider):
    name = "icims"
    allowed_domains = ["icims.com"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25 # seconds
    }

    def __init__(self, name=None, **kwargs):      
        self.start_urls = [f"{url['url']}" 
            for url 
            in json.load(open(ICIMS_JOB_URLS))]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(f'{url}', callback=self.parse_company, meta={'url' : f'{url}'})


    def parse_company(self, response):
        url = response.meta.get('url')
        meta={
            'company_url': response.xpath("//table//a/@href")[0].extract(),
            'company_logo': response.xpath("//table//img/@src")[0].extract(),
            'url': url
        }
        yield scrapy.Request(f"{url}jobs/search?pr=0&schemaId=&o=&in_iframe=1", callback=self.paginate, dont_filter=True, meta=meta)

    def paginate(self, response):
        last_link = response.xpath("//div[@class='iCIMS_Paging text-center']/a/@href")[-1].extract()
        last = int(last_link.split('h?pr=')[1].split('&')[0])+1
        url = response.meta.get('url')
        for index in range(0, last):
            href =  f"{url}jobs/search?pr={index}&schemaId=&o=&in_iframe=1"
            yield scrapy.Request(href, callback=self.parse, dont_filter=True, meta=response.meta)


    def parse(self, response):
        job_links = response.xpath("//div[contains(@class,'row')]/div/a/@href")
        for job_link in job_links:
            href = job_link.extract()
            response.meta['url'] = href
            yield scrapy.Request(href, callback=self.parse_thread, dont_filter=True, meta=response.meta)

    def parse_thread(self, response):
        company_url = response.meta.get('company_url')
        company_logo = response.meta.get('company_logo')
        url = response.meta.get('url').replace('?in_iframe=1','')
        icims_sd =  json.loads(response.text.split('var icimsSD = ')[1].split(";")[0])
        description = utils.clean_html(response.xpath("//div[contains(@class,'iCIMS_MainWrapper')]")[0].extract())
        raw =[r.extract() for r in response.xpath('//ul[1]/li')]
        job = JobItem(
            application_link= url,
            job_title = response.css("h1::text").get(),
            city = (',').join(icims_sd['job']['location'].split(',')[:2]),
            country = [icims_sd['job']['location'].split(',')[-1]],
            company_name = icims_sd['companyName'],
            description = description,
            company_link= company_url,
            company_logo= company_logo,
            job_type=utils.get_job_type(description),
            location_type=utils.get_workplace_type(description),
            date_posted= None,
            salary = utils.get_salary(description),
            requirements_raw = f'<ul>{("").join(raw)}</ul>',
            requirements_summary= f'<ul>{("").join(raw)}</ul>',
        )
        yield job
        
        
       
