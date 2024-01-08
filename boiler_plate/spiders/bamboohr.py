import scrapy
import json


class SmartrecruitersSpider(scrapy.Spider):

    name = "bamboohr"
    allowed_domains = ["bamboohr"]
    start_urls = ["https://reemahealth.bamboohr.com/careers/list"]
    base_url = 'https://reemahealth.bamboohr.com/careers/'

    def parse(self, response):
        jobs_list = json.loads(response.text)
       
        for job_data in jobs_list['result']:
            yield scrapy.Request(f'{self.base_url}{job_data['id']}/detail', callback=self.parse_thread, dont_filter=True, meta={'url': f'{self.base_url}{job_data['id']}'})

    def parse_thread(self, response):
        url = response.meta.get('url')
        job_json = json.loads(response.text)
        job_name = job_json['result']['jobOpening']['jobOpeningName']
        job_departament = job_json['result']['jobOpening']['departmentLabel']
        job_status = job_json['result']['jobOpening']['employmentStatusLabel']
        job_country = job_json['result']['jobOpening']['location']['addressCountry']
        job_city = job_json['result']['jobOpening']['location']['city']
        job = {"url": url, "job_title": job_name,  "job_departament": job_departament
        , "job_city": job_city
        }
        print(job)
        yield job
        
        
       
