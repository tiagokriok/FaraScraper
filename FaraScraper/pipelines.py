# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FarascraperPipeline(object):
    def process_item(self, item, spider):

        country = item['url'].split(",")[-1]

        item['country'] = country

        item['url'] = 'https://efile.fara.gov/ords/' + item['url']


        return item
