import scrapy
import json
import sys
import os
sys.path.append('jobs_ai/spiders/utils') #my machine...
sys.path.append('utils')
import utils

# insite: bamboohr.com "Current Openings"
# "Powered by BambooHR"

from utils import JobItem


BAMBOORH_JOB_URLS = os.path.join(os.path.dirname(__file__),'bamboohr_job_urls.json')

def get_qualifications(description):
    try:
        qualifications_list = description.split('Qualifications')[1].split('<ul>')[1].split('</ul>')[0].split('<li>')
        return [qualification.replace('</li>','') for qualification in qualifications_list]
    except:
        return []


class BamboohrRecruitersSpider(scrapy.Spider):

    name = "bamboohr"
    allowed_domains = ["bamboohr"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.25 # seconds
    }

    def __init__(self, name=None, **kwargs):      
        self.start_urls = [f"{url['url']}" 
            for url 
            in json.load(open(BAMBOORH_JOB_URLS))]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(f'{url}careers/company-info', callback=self.parse_company, meta={'url' : f'{url}'})

    def parse_company(self, response):
        url = response.meta.get('url')
        company = json.loads(response.text)
        meta={
            'company_name': company['result']['name'],
            'company_logo': company['result']['logoUrl'],
            'url': f"{url}careers/"
        }
        yield scrapy.Request(f"{url}careers/list", callback=self.parse, dont_filter=True, meta=meta)

    
    def parse(self, response):
        jobs_list = json.loads(response.text)
        base_url = response.meta.get('url')
        
        for job_data in jobs_list['result']:
            response.meta['url'] = f"{base_url}{job_data['id']}"
            yield scrapy.Request(f"{base_url}{job_data['id']}/detail", callback=self.parse_detail, dont_filter=True, meta=response.meta)
    

    def parse_detail(self, response):
        url = response.meta.get('url')
        company_name = response.meta.get('company_name')
        company_logo = response.meta.get('company_logo')
        job_json = json.loads(response.text)
        qualifications = get_qualifications(job_json['result']['jobOpening']['description'])
        requirements_raw = ('').join([f"<li>{qualification}</li>" for qualification in qualifications])
        job = JobItem(
            company_name = company_name,
            company_link= None,
            company_logo= company_logo,
            job_title = job_json['result']['jobOpening']['jobOpeningName'],
            description =  job_json['result']['jobOpening']['description'],
            city = job_json['result']['jobOpening']['atsLocation']['city'],
            country = job_json['result']['jobOpening']['atsLocation']['country'],
            job_type=utils.get_job_type(job_json['result']['jobOpening']['employmentStatusLabel']),
            location_type=utils.get_workplace_type(job_json['result']['jobOpening']['jobOpeningName']),
            date_posted= None,
            application_link= url,
            salary = utils.get_salary(job_json['result']['jobOpening']['description']),
            requirements_raw = f"<ul>{requirements_raw}</ul>",
            requirements_summary= qualifications,
        )
        yield job
        
        
       
