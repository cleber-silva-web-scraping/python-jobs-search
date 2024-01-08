import scrapy


class SmartrecruitersSpider(scrapy.Spider):

    name = "smartrecruiters"
    allowed_domains = ["smartrecruiters"]
    start_urls = ["https://careers.smartrecruiters.com/Square/api/more?page=1"]
    page = 1

    def parse(self, response):
        job_links = response.css(".link--block::attr(href)").getall()
        for job_link in job_links:
            yield scrapy.Request(job_link, callback=self.parse_thread, dont_filter=True, meta={'url': job_link})

    def parse_thread(self, response):
        url = response.meta.get('url')
        job_title = response.css(".job-title::text").get()
        job_detail = response.css(".job-detail::text").get()
        country = response.xpath("//meta[@itemprop='addressCountry']/@content")[0].extract()
        
        job = {"url": url, "title": job_title, "job_detail": job_detail, "country": country}
        yield job
        
        
       
