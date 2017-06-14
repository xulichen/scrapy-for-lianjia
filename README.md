# scrapy-for-lianjia

 Python == 3.6    scrapy == 1.4.0

# 基于scrapy框架下的链家网Python爬虫

  在测试中遇到headers里加入User-Agent会导致页面重定向
去掉User-Agent即能够很好的抓取链家网数据

  链家网的租房房源数据已在源代码中可见，因此无需查找API及相应的Json和XML数据

  链家网的搜索结果只显示100页，但实际上存在更多的内容，根据房源总数可以推断总页数并进行数据的爬取

  该爬虫较好的运用re及xpath对数据进行了筛选整理，有效地存入Mongo数据库库
