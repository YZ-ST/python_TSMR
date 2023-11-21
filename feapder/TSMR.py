import time
import datetime
from playwright.sync_api import Page
import feapder
from feapder.utils.webdriver import PlaywrightDriver
import ddddocr
import requests
import re
from modules import logger

class TestPlaywright(feapder.AirSpider):
    # 自定义配置
    def __init__(self, depart_station, arrive_station, book_ticket_time, depart_time, ticket_amount, end_time, national_ID, phonenumber, email, to_go_account):
        super().__init__()
        self.depart_station = depart_station
        self.arrive_station = arrive_station
        self.book_ticket_time = book_ticket_time
        self.depart_time = depart_time
        self.ticket_amount = ticket_amount
        self.end_time = end_time
        self.national_ID = national_ID
        self.phonenumber = phonenumber
        self.email = email
        self.to_go_account = to_go_account
        self.ticket = None  # 定票代碼
        
    __custom_setting__ = dict(
        RENDER_DOWNLOADER="feapder.network.downloader.PlaywrightDownloader",
        PLAYWRIGHT=dict(
            headless=True,  # 是否为无头浏览器
        ),
        SPIDER_MAX_RETRY_TIMES=1,
    )

    def start_requests(self):
        yield feapder.Request("https://irs.thsrc.com.tw/IMINT/?locale=tw", render=True)

    def parse(self, reqeust, response):
        driver: PlaywrightDriver = response.driver
        page: Page = driver.page

        # 點級同意
        page.click("#cookieAccpetBtn")
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        # Function to perform the booking process
        def ocr_security(url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                with open('tsmr.jpg', 'wb') as file:
                    file.write(response.content)
                logger.info("照片已成功下載!")
            else:
                logger.info(f"獲取圖片失敗，HTTP響應碼：{response.status_code}")

            # # 驗證碼
            ocr = ddddocr.DdddOcr()

            with open("tsmr.jpg", 'rb') as f:
                image = f.read()

            security_code = ocr.classification(image)
            logger.info(f"security_code = {security_code}")
            return security_code
        def perform_booking():
            # 出發站
            click_button = page.locator("select[name='selectStartStation']")
            click_button.click()
            click_button.select_option(self.depart_station)
            time.sleep(1)

            # 到達站
            click_button = page.locator("select[name='selectDestinationStation']")
            click_button.click()
            click_button.select_option(self.arrive_station)
            time.sleep(1)

            # 出發日期
            current_date = datetime.date.today()
            # 将用户预订时间字符串转换为日期对象
            self.book_ticket_time = datetime.datetime.strptime(str(self.book_ticket_time), "%Y-%m-%d").date()

            if self.book_ticket_time.month > current_date.month:
                logger.info("訂票日期和當前日期不在同一個月份，訂票日期是{}月，當前日期是{}月。".format(self.book_ticket_time.month, current_date.month))
                input_date = datetime.datetime.strptime(str(self.book_ticket_time), "%Y-%m-%d")
                formatted_date = input_date.strftime("%B %d, %Y")
                logger.info("formatted_date", formatted_date)
                page.get_by_role("textbox").first.click()
                page.locator(".flatpickr-next-month").first.click()
                # 去除日期中的0
                dt = datetime.datetime.strptime(formatted_date, "%B %d, %Y")
                formatted_book_ticket_time = "{} {}, {}".format(dt.strftime("%B"), dt.day, dt.year)
                logger.info(f"formatted_book_ticket_time = {formatted_book_ticket_time}")
                page.get_by_label(formatted_book_ticket_time).first.click() 
            else:
                logger.info("訂票日期和當前日期在同一個月份，都是{}月。".format(self.book_ticket_time.month))
                input_date = datetime.datetime.strptime(str(self.book_ticket_time), "%Y-%m-%d")
                formatted_date = input_date.strftime("%B %d, %Y")
                logger.info("formatted_date", formatted_date)
                page.get_by_role("textbox").first.click()
                # 去除日期中的0
                dt = datetime.datetime.strptime(formatted_date, "%B %d, %Y")
                formatted_book_ticket_time = "{} {}, {}".format(dt.strftime("%B"), dt.day, dt.year)
                logger.info(f"formatted_book_ticket_time = {formatted_book_ticket_time}")
                page.get_by_label(formatted_book_ticket_time).first.click()
            time.sleep(1)

            # 購票數量
            click_button = page.locator("select[name='ticketPanel:rows:0:ticketAmount']")
            click_button.click()
            click_button.select_option(self.ticket_amount)
            time.sleep(1)

            # 出發時間
            click_button = page.locator("select[name='toTimeTable']")
            click_button.click()
            click_button.select_option(self.depart_time)
            time.sleep(1)

            
            # 使用选择器选择<img>标签
            img_element = page.query_selector('#BookingS1Form_homeCaptcha_passCode')
            
            # # 驗證碼
            # 获取<img>标签的src属性值
            src_attribute = img_element.get_attribute('src')
            logger.info("src属性值:", src_attribute)
            url = "https://irs.thsrc.com.tw/" + src_attribute
            securityCode = ocr_security(url)
            page.type("#securityCode", securityCode)

            # 提交
            page.click("#SubmitButton")

        def clean_text(text):
            # 使用split()方法分割文本，并去除不需要的空白字符
            cleaned_text = ' '.join(text.split())
            return cleaned_text
        
        def perform_booking_2():
            logger.info("進入第二頁訂票")
            time.sleep(3)
            # 第一個塞選條件: 找出適合的時間
            time_elements = page.query_selector_all('div.mobile-wrapper')
            data_dict  =  []
            for elements in time_elements:
                elements = str(elements.text_content())
                element_text = clean_text(elements)
                # logger.info(f"element_text = {element_text}")
                
                data_dict.append(element_text)
            logger.info(f"data_dict = {data_dict}")
            
            # 解析元素文本并存储到列表中
            element_data = []
            for element_text in data_dict:
                match = re.match(r'(\d{2}:\d{2}) (\d{2}/\d{2}) arrow_right_alt (\d{2}:\d{2}) schedule(\d+:\d+) ｜ directions_railway(\d+)', element_text)
                if match:
                    start_time, date, end_time, schedule, direction = match.groups()
                    element_data.append({
                        "start_time": start_time,
                        "date": date,
                        "end_time": end_time,
                        "schedule": schedule,
                        "direction": direction
                    })

            # 第一个条件：筛选时间在起始时间和结束时间之间的元素
            start_time_filter = self.depart_time
            end_time_filter = self.end_time
            filtered_elements = [element for element in element_data if start_time_filter <= element["start_time"] <= end_time_filter]

            logger.info(f"filtered_elements_1 = {filtered_elements}")

            # 第二个条件：找到最短的schedule
            filtered_elements.sort(key=lambda x: x["schedule"])

            logger.info(f"filtered_elements_2 = {filtered_elements}")

            # 第三个条件：取结果的第一项并打印时间、班次和方向
            if filtered_elements:
                first_result = filtered_elements[0]
                logger.info(f"时间：{first_result['start_time']} - {first_result['end_time']}")
                logger.info(f"班次：{first_result['schedule']}")
                logger.info(f"班次：{first_result['direction']}")
            else:
                raise Exception("沒有符合的車次")
            
            page.locator(f'input[QueryCode="{first_result["direction"]}"]').click()
            time.sleep(1)
            page.locator(f'input[name="SubmitButton"]').click()
        
        def perform_booking_3():
            logger.info("進入第三頁訂票")
            time.sleep(1)
            page.type("#idNumber", self.national_ID)
            time.sleep(1)
            page.type("#mobilePhone", self.phonenumber)
            time.sleep(1)
            page.type("#email", self.email)
            time.sleep(1)
            page.locator(f'input[id="memberSystemRadio1"]').click()
            time.sleep(1)
            page.type("#msNumber", self.to_go_account)
            time.sleep(1)
            # page.locator(f'input[name="TicketMemberSystemInputPanel:TakerMemberSystemDataView:memberSystemRadioGroup:memberSystemShipCheckBox"]').click()
            time.sleep(1)
            page.locator(f'input[name="agree"]').click()
            time.sleep(1)
            
            page.locator(f'input[id="isSubmit"]').click()
            time.sleep(3)
            
            # 最後要送出 
            page.locator(f'input[name="SubmitButton"]').click()
            time.sleep(2)
            
            # 進入第四頁
            logger.info("進入第四頁訂票")
            pnr_code_element = page.query_selector("p.pnr-code > span").text_content()
            logger.debug(f"pnr_code_element = {pnr_code_element}")
            self.ticket = pnr_code_element
            logger.info("訂票成功")
            
            
        # Set a maximum number of retries
        max_retries = 3
        retries = 0
        while retries < max_retries:
            perform_booking()
            # 若出現驗證碼錯誤，重新retry一次網頁
            time.sleep(2)
            
            # 检查是否存在具有 'h2.form-title' 类的元素
            form_title_element = page.query_selector('h2.form-title')
            if form_title_element:
                if form_title_element.inner_text() == "訂位明細":
                    logger.info("驗證碼輸入成功")
                    break

            # 检查是否存在具有 'span.feedbackPanelERROR' 类的元素
            feedback_panel_element = page.query_selector('span.feedbackPanelERROR')
            logger.info(f"feedback_panel_element = {feedback_panel_element}")
            if feedback_panel_element:
                error_message = feedback_panel_element.inner_text()
                if error_message == "檢測碼輸入錯誤，請確認後重新輸入，謝謝！":
                    logger.info("檢測碼輸入錯誤，請確認後重新輸入，謝謝！")
                    retries += 1
                    logger.info(f"訂票失敗_Retry:{retries}")
                    if retries == max_retries:
                        raise Exception("驗證碼連續三次輸入錯誤，離開訂票系統！!")
                    # 可以在这里添加等待一段时间后重试的代码
                    time.sleep(2)
                    
                elif error_message == "去程查無可售車次或選購的車票已售完，請重新輸入訂票條件。":
                    logger.info("去程查無可售車次或選購的車票已售完，請重新輸入訂票條件。")
                    raise Exception("去程查無可售車次或選購的車票已售完，請重新輸入訂票條件。")

        perform_booking_2()
        perform_booking_3()
        
    def run(self):
        super().run()

#============================================================================================#

def TSMR_main(depart_station, arrive_station, book_ticket_time, depart_time, ticket_amount, end_time, national_ID, phonenumber, email, to_go_account):
    try:
        logger.info(f"depart_station= {depart_station}")
        logger.info(f"arrive_station= {arrive_station}")
        logger.info(f"book_ticket_time= {book_ticket_time}")
        logger.info(f"depart_time= {depart_time}")
        logger.info(f"ticket_amount= {ticket_amount}")
        logger.info(f"end_time= {end_time}")
        logger.info(f"national_ID= {national_ID}")
        logger.info(f"phonenumber= {phonenumber}")
        logger.info(f"email= {email}")
        logger.info(f"to_go_account= {to_go_account}")
        # depart_station = "台北"
        # arrive_station = "台中"
        # book_ticket_time = "2023-10-11"
        # depart_time = "13:00"
        # ticket_amount = "1"
        # end_time = "15:30"
        # national_ID =  "A123456789"
        # phonenumber = "0983636056"
        # email = "pp0975320034@gmail.com"
        # to_go_account = None
        
        current_date = datetime.date.today()
        book_ticket_time = datetime.datetime.strptime(book_ticket_time, "%Y-%m-%d").date()
        if book_ticket_time < current_date:
            raise Exception("購票日期不得小於今日日期")
        # 計算28天後的日期
        twenty_eight_days_later = current_date + datetime.timedelta(days=28)
        if book_ticket_time > twenty_eight_days_later:
            raise Exception("錯誤訊息:book_ticket_date 大於 current_date 的28天內")

        if to_go_account == "":
            to_go_account = "GG21225905"
            
        spider = TestPlaywright(depart_station, arrive_station, book_ticket_time, depart_time, ticket_amount, end_time, national_ID, phonenumber, email, to_go_account)
        spider.run()
        ticket = spider.ticket
        return ticket
    except Exception as e:
        logger.info(e)





if __name__ == "__main__":
    depart_station = "台北"
    arrive_station = "台中"
    book_ticket_time = "2023-11-22"
    depart_time = "13:00"
    ticket_amount = "1"
    end_time = "15:30"
    national_ID =  "A123456789"
    phonenumber = ""
    email = ""
    to_go_account = ""
    ticket = TSMR_main(depart_station, arrive_station, book_ticket_time, depart_time, ticket_amount, end_time, national_ID, phonenumber, email, to_go_account)
    logger.info(f"ticket = {ticket}")