# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class BossScrapyPipeline(object):

    def __init__(self):
        self.client = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='boss',
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        # 工作名称 工作城市 工作经验 学历要求 公司名字 公司所在地
        job_name = item['job_name']
        job_city = item['job_city']
        job_experience = item['job_experience']
        job_education = item['job_education']
        company_name = item['company_name']
        loc_job = item['loc_job']
        # 公司介绍 职位描述 团队介绍 工商信息
        company_describe_detail = item['company_describe_detail']
        job_describe_detail = item['job_describe_detail']
        team_describe_detail = item['team_describe_detail']
        business_information = item['business_information']

        lis = [
            job_name, job_city, job_experience, job_education, company_name, loc_job,
            company_describe_detail, job_describe_detail, team_describe_detail,
            business_information
        ]

        sql = 'insert into company_detail(工作名称,工作城市,工作经验,学历要求,' \
              '公司名字,公司所在地,公司介绍,职位描述,团队介绍,工商信息) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cur.execute(sql, lis)
        self.client.commit()

        return item
