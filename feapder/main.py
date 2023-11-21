
# 引入 LINE Bot 聊天機器人會使用到的函式庫
from flask import Flask, request, abort, render_template
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)
from TSMR import TSMR_main
from modules import logger

app = Flask(__name__)

# 驗證是否有使用 LINE Bot 聊天機器人的使用權限
line_bot_api = LineBotApi('HQg/O0DG46vWhd6NZOUf4Gmg3gQPfei3Ybk67X2T+kHBuQOObM8m8ZPMg9shBu0Wt5bf4oHrCatI14pBWEFCUZgzjCNNfQ4A/VJ7kg5UBg/Q8N0YSDnJlBLGXkYs2zwYqUx8oLRbOthC4+Y4q1MHJQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('740e087d9d7717ff7092eaf5ba835b41')

# 1. 要修改ngrok的網址 2. 在line_bot修改ngrok的網址 3. 要從line打開連結，才能讓ngrok知道是哪個user
ngrok_url = "https://6b3c-159-117-82-41.ngrok-free.app"


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/err")
def err():
    return render_template('err.html')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/crawler_TSMR", methods=['POST'])
def crawler_TSMR():
    # 傳入表單參數
    user_id = request.form.get('user_id')
    depart_station = request.form.get('depart_station')
    arrive_station = request.form.get('arrive_station')
    book_ticket_time =  request.form.get('book_ticket_time')
    depart_time = request.form.get('depart_time')
    ticket_amount = request.form.get('ticket_amount')
    end_time = request.form.get('end_time')
    national_ID =  request.form.get('national_ID')
    phonenumber = request.form.get('phonenumber')
    email = request.form.get('email')
    to_go_account = request.form.get('to_go_account')
    
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
    
    if user_id != None:
        logger.debug("user_id: {user_id}")
    ticket = TSMR_main(depart_station, arrive_station, book_ticket_time, depart_time, ticket_amount, end_time, national_ID, phonenumber, email, to_go_account)
    message = TextSendMessage(text=f"您的訂票代碼為：{ticket}\n請於30分鐘內完成付款，否則訂票將會失效")
    line_bot_api.push_message(user_id, messages=message)
    # return "<p1>填寫成功，您的訂票代碼為：'+ticket+'</p1><br><p2>請於30分鐘內完成付款，否則訂票將會失效</p2>"
    return ticket


# 所有從 LINE 傳來的事件都會先經過這個路徑
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 接收事件後，會根據定義的行為做相應處理（業務邏輯）
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    
    if event.message.text == '填寫訂票資訊':
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(
            alt_text='hello',
            contents = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "action": {
                    "type": "uri",
                    "uri": "http://linecorp.com/"
                    }
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "text": "訂票小助手",
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "填寫完訂票資訊並送出後，1分鐘左右將會傳送訂位代號給您",
                            "color": "#666666",
                            "flex": 5,
                            "size": "sm",
                            "margin": "sm",
                            "wrap": True
                        }
                        ]
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "height": "sm",
                        "action": {
                        "type": "uri",
                        "uri": f"{ngrok_url}?user_id="+user_id,
                        "label": "填寫訂票資訊"
                        }
                    }
                    ],
                    "flex": 0
                }
            }
        ))


if __name__ == "__main__":
    app.run(debug=True, port=8000)