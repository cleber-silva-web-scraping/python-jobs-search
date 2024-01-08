import scrapy
import json


class SmartrecruitersSpider(scrapy.Spider):

    name = "oraclecloud"
    allowed_domains = ["oraclecloud.com"]
    start_urls = ["https://eevd.fa.us6.oraclecloud.com/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations,flexFieldsFacet.values&finder=findReqs;siteNumber=CX,facetsList=LOCATIONS%3BWORK_LOCATIONS%3BWORKPLACE_TYPES%3BTITLES%3BCATEGORIES%3BORGANIZATIONS%3BPOSTING_DATES%3BFLEX_FIELDS,limit=25,sortBy=POSTING_DATES_DESC"]
    base_url =  'https://eevd.fa.us6.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX/requisitions/preview/'
    def parse(self, response):
        jobs_list = json.loads(response.text)
       
        for job_data in jobs_list['items'][0]['requisitionList']:
            url = f'{self.base_url}{ job_data['Id']}'
            job_name = job_data['Title']
            location = job_data['PrimaryLocation']
            country = job_data['PrimaryLocationCountry']
            work_type = job_data['WorkplaceType']
            job = {
                'job_name' :job_name,
                'location' :location,
                'country' :country,
                'type' :work_type,
            }
            print(job)
            yield job

   
        
        
       
