import scrapy
from elest.items import ElestItem

class ElebestSpider(scrapy.Spider):
    name = 'elebest'
    allowed_domains = ['www.11st.co.kr']
    start_urls = ['http://www.11st.co.kr/']

    def start_requests(self):
        url = "https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain"
        yield scrapy.Request(url=url, callback=self.parse_main)

    # 카테고리의 세부 url을 얻는 중간 단계
    def parse_main(self, response):
        ca_link = response.css("div.best_category_box > ul > li button::attr(onclick)").getall()
        ca_name = response.css("div.best_category_box > ul > li button::text").getall()
        sub_link = response.css("div.sub_category_box > ul > li a::attr(onclick)").getall()
        sub_name = response.css("div.sub_category_box > ul > li a::text").getall()

        # 세부 카테고리들의 베스트 상품만 크롤링
        for index, link in enumerate(sub_link):
            link_first = link.find("(")
            link_last = link.find(")")

            link = link[link_first+1:link_last].split(",")
            url = "http://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&cornerNo={}&dispCtgrNo={}".format(link[0], link[1])
            yield scrapy.Request(url=url, callback=self.parse_items, meta={"maincategory_name": ca_name[int(link[0])], "subcategory_name": sub_name[index]})

        # 대표카테고리의 베스트 200도 크롤링 하고 싶다면 아래 코드 추가
        # for index, link in enumerate(ca_link):
            # link_first = link.find("(")
            # link_last = link.find(")")
            # link = link[link_first+1:link_last]
            # yield scrapy.Request(url ="http://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&cornerNo="+link,
            # callback=self.parse_items, meta={"maincategory_name":ca_name[index], "subcategory_name":"ALL"})


    def parse_items(self, response):
        best_items = response.css("ul.cfix ")[1].css("li")
        for s, item in enumerate(best_items):
            doc = ElestItem()
            main_category=response.meta["maincategory_name"]
            sub_category = response.meta["subcategory_name"]
            ranking = s+1
            title = item.css("a p::text").get()
            price = item.css("strong.sale_price::text").get()
            seller = item.css("div.store a::text").get()
            link = item.css("div a::attr(href)").get()
            doc["main_category"] =  main_category
            doc["sub_category"] =sub_category
            doc["ranking"] =  ranking
            doc["title"] =  title
            doc["price"] = price
            doc["seller"] = seller
            doc["link"] = link

            yield doc


    def parse(self, response):
        pass
