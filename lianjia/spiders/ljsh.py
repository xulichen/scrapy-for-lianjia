# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re

from lianjia.items import LianjiaItem


class LjshSpider(scrapy.Spider):
    name = 'ljsh'
    start_url = 'http://sh.lianjia.com/zufang/d{page}rs{location}'
    location = '普陀'

    def start_requests(self):
        yield Request(url=self.start_url.format(page=1, location=self.location), callback=self.parse_index)

    def parse_index(self, response):
        sel = response.selector
        #使用xpath抓取租房数据
        title = sel.xpath('.//div[@class="info-panel"]/h2/a/text()').extract()
        condition3 = sel.xpath('.//div[@class="col-1"]/div[1]/a/span[1]/text()').extract()
        room_compose = sel.xpath('.//div[@class="col-1"]/div[1]/span[1]/text()').extract()
        room_spare = sel.xpath('.//div[@class="col-1"]/div[1]/span[2]/text()').extract()
        condition1 = sel.xpath('.//div[@class="col-1"]/div[2]//a[1]/text()').extract()
        condition2 = sel.xpath('.//div[@class="col-1"]/div[2]//a[2]/text()').extract()
        floor = sel.xpath('.//div[@class="col-1"]/div[2]/div/text()').re('[^\\n\\t]+/[^\\n\\t]+')
        #有些房子的朝向及subway是没有填写的，后续需要进一步判断
        direction = sel.xpath('.//div[@class="col-1"]/div[2]/div/text()[5]').re('[^\\n\\t]+')
        subway = sel.xpath('.//div[@class="col-1"]//span[@class="fang-subway-ex"]/span/text()').extract()
        price = sel.xpath('.//div[@class="col-3"]/div[@class="price"]/span/text()').extract()
        #所得上传时间的格式需要进一步处理
        upload = sel.xpath('.//div[@class="col-3"]/div[@class="price-pre"]/text()').extract()
        lookat_num = sel.xpath('.//div[@class="col-2"]//span[@class="num"]/text()').extract()
        items = LianjiaItem()
        #nf = 'not find' nff nfd nfs为未填写楼层、朝向及subway的数量
        nff = 0
        nfd = 0
        nfs = 0
        for i in range(0,len(title)):
            items['title'] = title[i]
            items['condition1'] = condition1[i]
            items['condition2'] = condition2[i]
            items['condition3'] = condition3[i]
            items['room_compose'] = room_compose[i].strip()
            items['room_spare'] = room_spare[i].strip()
            items['price'] = price[i]
            items['upload'] = re.sub(r'\s+', '', upload[i])
            items['lookat_num'] = lookat_num[i]
            #判断该房子的信息中是否含有楼层标签
            if sel.xpath('.//ul[@id="house-lst"]/li[{}]//div[@class="col-1"]/div[2]/div/text()'.format(i+1)).re('[^\\n\\t]+/[^\\n\\t]+'):
                items['floor'] = floor[i-nff]
            else:
                items['floor'] = 'not find'
                nff = nff +1
            # 判断该房子的信息中是否含有朝向标签
            if sel.xpath('.//ul[@id="house-lst"]/li[{}]//div[@class="col-1"]/div[2]/div/text()[5]'.format(i+1)).re('[^\\n\\t]+'):
                items['direction'] = direction[i-nfd]
            else:
                items['direction'] = 'not find'
                nfd = nfd + 1
            #判断该房子的信息中是否含有subway标签
            if sel.xpath('.//ul[@id="house-lst"]/li[{}]//div[@class="col-1"]//span[@class="fang-subway-ex"]/span/text()'.format(i+1)).extract_first():
                items['subway'] = subway[i-nfs]
            else:
                items['subway'] = 'not find'
                nfs = nfs + 1
            yield items

        #房源总数 / 每页20 = 总页数
        total_num = sel.xpath('/html/body/div[4]/div[2]/div/div[1]/h2/span/text()').extract_first()
        total_page = int(int(total_num)/20)
        for i in range(2, total_page):
            yield Request(url=self.start_url.format(page=i, location=self.location), callback=self.parse_index)



        


        

