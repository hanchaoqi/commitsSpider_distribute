# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from commitsSpider.items import CommitsspiderItem
from scrapy_redis.spiders import RedisMixin
import re

class GithubspiderSpider(RedisMixin,CrawlSpider):
    name = 'githubSpider'
    allowed_domains = ['github.com']
    patt = re.compile('cve-\d{4}-\d{4}',re.I)
    redis_key = 'githubSpider:start_urls'    

    def __init__(self,software):
        self.software = software
        if software == "linux":
            #self.start_urls = ['https://github.com/torvalds/%s/commits/master' % software,'https://github.com/torvalds/%s/commits/master?page=101' % software]
            self.rules =[ 
            Rule(LinkExtractor(allow=('https://github.com/torvalds/linux/commits/master\?page=\d+'),restrict_xpaths=('//div[@class="pagination"]/a[last()]'))),
            Rule(LinkExtractor(allow=('/torvalds/linux/commit/[a-f0-9]+'),restrict_xpaths=('//a[@class="message"]')), callback='parse_item'),
            ]
        super(GithubspiderSpider,self).__init__()

    def _set_crawler(self,crawler):
        CrawlSpider._set_crawler(self,crawler)
        RedisMixin.setup_redis(self)

    def parse_item(self, response):
        item = CommitsspiderItem()
        rawText = "".join(response.xpath('//p[@class="commit-title"]/text()|//div[@class="commit-desc"]/pre/text()|//div[@id="files"]').extract())
        item['cve'] = self.patt.findall(rawText)
        if len(item['cve']) != 0:
            item['url'] = response.url
            return item
