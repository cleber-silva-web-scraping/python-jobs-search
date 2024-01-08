import scrapy
import json


class SmartrecruitersSpider(scrapy.Spider):

    name = "applytojob"
    allowed_domains = ["applytojob.com"]
    start_urls = ["https://caden.applytojob.com/apply/"]

    def parse(self, response):
        job_links = response.xpath("//li[contains(@class,'list-group-item')]/h4/a/@href")
       
        for job_link in job_links:
            href = job_link.extract()
            yield scrapy.Request(href, callback=self.parse_thread, dont_filter=True, meta={'url': href})

    def parse_thread(self, response):
        url = response.meta.get('url')
        job_name = response.css("h1::text").get()
        job_country = response.xpath("//div[@title='Location']/text()")[1].extract()
        job = {"url": url, "job_title": job_name,  "job_country": job_country.strip()}
        print(job)
        yield job
        
        
       
