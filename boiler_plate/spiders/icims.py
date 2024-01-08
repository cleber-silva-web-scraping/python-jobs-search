import scrapy
import json


class SmartrecruitersSpider(scrapy.Spider):

    name = "icims"
    allowed_domains = ["icims"]
    start_urls = ["https://careers-aeieng.icims.com/jobs/search?pr=0&schemaId=&o=&in_iframe=1"]

    def parse(self, response):
        job_links = response.xpath("//div[contains(@class,'row')]/div/a/@href")
       
        for job_link in job_links:
            href = job_link.extract()
            yield scrapy.Request(href, callback=self.parse_thread, dont_filter=True, meta={'url': href})

    def parse_thread(self, response):
        url = response.meta.get('url').replace('?in_iframe=1','')
        job_name = response.css("h1::text").get()
        job_country = response.xpath("//dd[contains(@class,'iCIMS_JobHeaderData')]/span/text()")[1].extract()
        job = {"url": url, "job_title": job_name,  "job_country": job_country}
        print(job)
        yield job
        
        
       
