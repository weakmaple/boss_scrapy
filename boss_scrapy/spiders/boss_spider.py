# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boss_scrapy.items import BossScrapyItem


class BossSpiderSpider(CrawlSpider):
    name = 'boss_spider'
    # allowed_domains = ['zhipin.com"']
    # start_urls = ['http://httpbin.org/']
    start_urls = ['https://www.zhipin.com/c101010100/?query=python%E7%88%AC%E8%99%AB&page=1&ka=page-1']

    rules = (
        Rule(LinkExtractor(allow=r'.+page=%d+&ka=page-%d+/'), follow=True),
        Rule(LinkExtractor(allow=r'.+/job_detail/.+\.html'), callback='parse_item', follow=False),
        # Rule(LinkExtractor(allow=r'http://httpbin.org/ip'), callback='parse_item'),
    )

    def parse_item(self, response):
        # print("="*40)
        # print(response.body)
        # print("=" * 40)
        job_name = response.xpath('//div[@class="name"]/h1/text()').get()
        job_detail = response.xpath('//div[@class="info-primary"]/p//text()').getall()
        job_city = job_detail[0]
        job_experience = job_detail[1]
        job_education = job_detail[2]
        company_name = response.xpath('//div[@class="info-company"]/h3/a/text()').get()
        loc_job = response.xpath('//div[@class="location-address"]/text()').get()

        job_secs = response.xpath('//div[@class="job-sec company-info"]/h3/text()').get()
        if job_secs == '公司介绍':
            company_describe_detail = response.xpath('//div[@class="job-sec company-info"]/div[@class="text"]/text()').getall()
            company_describe_detail = '\n'.join(company_describe_detail).strip()
        else:
            company_describe_detail = '无'

        job_secs = response.xpath('//div[@class="job-sec"]')
        job_describe_detail,team_describe_detail,business_information = '无','无','无'
        for job_sec in job_secs:
            sec_describe = job_sec.xpath('./h3/text()').get()
            if sec_describe == '职位描述':
                job_describe_detail = job_sec.xpath('./div[@class="text"]/text()').getall()
                job_describe_detail = '\n'.join(job_describe_detail).strip()

            if sec_describe == '团队介绍':
                team_describe_detail = job_sec.xpath('./div[@class="text"]/text()').getall()
                team_describe_detail = '\n'.join(team_describe_detail).strip()

            if sec_describe == '工商信息':
                business_information_1 = job_sec.xpath('./div[@class="name"]/text()').getall()
                business_information_1 = ''.join(business_information_1).strip()
                business_information_2 = job_sec.xpath('./div[@class="level-list"]/li//text()').getall()
                business_information_2 = '\n'.join(business_information_2).strip()
                business_information = business_information_1+'\n'+business_information_2

        item = BossScrapyItem(
            job_name =  job_name,
            job_city = job_city,
            job_experience = job_experience,
            job_education = job_education,
            company_name = company_name,
            loc_job = loc_job,
            company_describe_detail = company_describe_detail,
            job_describe_detail = job_describe_detail,
            team_describe_detail = team_describe_detail,
            business_information = business_information
        )

        yield item




