import scrapy


class SmartrecruitersSpider(scrapy.Spider):

    name = "recruitee"
    allowed_domains = ["recruitee.com"]
    start_urls = ["https://distilled.recruitee.com/"]
    base_url = 'https://distilled.recruitee.com'

    def parse(self, response):
        job_links = response.xpath("//div[@data-testid='offer-list-grid']//a/@href")
        for job_link in job_links:
            href = job_link.extract()
            yield scrapy.Request(f'{self.base_url}{href}', callback=self.parse_thread, dont_filter=True, meta={'url': f'{self.base_url}{href}'})

    def parse_thread(self, response):
        url = response.meta.get('url')
        job_title = response.xpath("//h1/text()")[0].extract().strip()
        job_location = response.xpath("//span[@class='custom-css-style-job-location-city']/text()")[0].extract()
        job_type = response.xpath("//span[@data-cy='department-name']/span/text()")[0].extract()
        job = {"url": url, "title": job_title, "job_location": job_location, "job_type": job_type}
        print(job)
        yield job
        
        
       
