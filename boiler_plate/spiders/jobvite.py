import scrapy


class SmartrecruitersSpider(scrapy.Spider):

    name = "jobvite"
    allowed_domains = ["jobvite.com"]
    start_urls = ["https://jobs.jobvite.com/careers/barracuda-networks-inc/jobs"]
    base_url = 'https://jobs.jobvite.com'

    def parse(self, response):
        job_links = response.xpath("//td[contains(@class,'jv-job-list-name')]/a/@href")
        for job_link in job_links:
            href = job_link.extract()
            yield scrapy.Request(f'{self.base_url}{href}', callback=self.parse_thread, dont_filter=True, meta={'url': f'{self.base_url}{href}'})

    def parse_thread(self, response):
        url = response.meta.get('url')
        job_title = response.xpath("//h2/text()")[0].extract().strip()
        job_type  = response.xpath("//p[contains(@class,'job-detail-meta')]/text()")[0].extract().strip()
        job = {"url": url, "title": job_title, "job_type": job_type}
        print(job)
        yield job
        
        
       
