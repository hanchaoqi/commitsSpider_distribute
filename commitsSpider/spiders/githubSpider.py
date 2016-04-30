# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from commitsSpider.items import CommitsspiderItem
import re

class GithubspiderSpider(CrawlSpider):
    name = 'githubSpider'
    allowed_domains = ['github.com']
    patt = re.compile('cve-\d{4}-\d{4}',re.I)

    def __init__(self,software):
        self.software = software
        if software == "linux":
            self.start_urls = ['https://github.com/torvalds/linux/commits/master?page=1']
            self.rules = (
        Rule(LinkExtractor(allow=r'https://github.com/torvalds/linux/commits/master\?page=\d+',restrict_xpaths=('//div[@class="pagination"]/a[last()]'))),
        Rule(LinkExtractor(allow=r'/torvalds/linux/commit/[a-f0-9]+',restrict_xpaths=('//p[@class="commit-title"]/a[@class="message"]')), callback='parse_item', follow=True),
        )
        super(GithubspiderSpider,self).__init__()
    def parse_item(self, response):
        item = CommitsspiderItem()
        rawText = response.xpath('//p[@class="commit-title"]/text()|//div[@class="commit-desc"]/pre/text()|//div[@id="files"]').extract()
        item['cve'] = self.patt.findall(rawText)
        if len(item) != 0:
            item['url'] = response.url
            yield item
        return
