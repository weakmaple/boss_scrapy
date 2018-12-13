# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BossScrapyItem(scrapy.Item):
    # 工作名称 工作城市 工作经验 学历要求 公司名字 公司所在地
    job_name = scrapy.Field()
    job_city = scrapy.Field()
    job_experience = scrapy.Field()
    job_education = scrapy.Field()
    company_name = scrapy.Field()
    loc_job = scrapy.Field()
    # 公司介绍 职位描述 团队介绍 工商信息
    company_describe_detail = scrapy.Field()
    job_describe_detail = scrapy.Field()
    team_describe_detail = scrapy.Field()
    business_information = scrapy.Field()

