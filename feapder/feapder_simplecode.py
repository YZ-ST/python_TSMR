import feapder

class FirstSpider(feapder.AirSpider):

    # 生產任務
    def start_requests(self):
        for page in range(1,3):
            print(f"page = {page}")
            yield feapder.Request(f"https://etherscan.io/tokens?ps=10&p={page}")
        

    # 解析數據                         
    def parse(self, request, response):
        for symbol in range(1,11):
            article_list = response.xpath(f'//*[@id="ContentPlaceHolder1_tblErc20Tokens"]/table/tbody/tr[{symbol}]/td[2]/a/div/div')
            for article in article_list:
                # title = article.xpath("./text()").extract_first()
                # url = article.xpath("./@href").extract_first()
                token = article.xpath("./text()").extract_first()
                print(token)


if __name__ == "__main__":
    FirstSpider().start()
