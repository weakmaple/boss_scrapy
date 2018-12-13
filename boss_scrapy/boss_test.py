import requests
from lxml import etree
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
   'user-agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
}

url = 'https://www.zhipin.com/c100010000-p100109/?page=1&ka=page-1/'
response = requests.get(url=url,headers=DEFAULT_REQUEST_HEADERS)
html = etree.HTML(response.text)

# print(response.text)
job_name = html.xpath('//div[@class="job-title"]/text()')
job_detail = html.xpath('//div[@class="info-primary"]/p//text()')
job_city = job_detail[0]
job_experience = job_detail[1]
job_education = job_detail[2]
print(job_name,job_city,job_experience,job_education)