from scrapy.spiders import Spider
import csv
from s_task.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://dmoz-odp.org/Arts/Music/Instruments/"
    ]

    def parse(self, response):
        sel = response.css('#sites-section > #site-list-content > div.site-item > div.title-and-desc')
        items = []
        for site in zip(sel.xpath('a/@href').extract(), sel.xpath('a/div/text()').extract()):
            item = Website()
            item['SiteName'] = site[1]
            item['Title'] = site[1]
            item['Url'] = site[0]
            items.append(item)
            if len(items) >= 10:
                break
        filename = "records.csv"
        keys = items[0].keys()
        with open(filename, 'w') as csvfile:
            dict_writer = csv.DictWriter(csvfile, keys)
            dict_writer.writeheader()
            dict_writer.writerows(items)
