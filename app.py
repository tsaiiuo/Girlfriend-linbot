from email.headerregistry import Address
from typing import Text
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('Y2TELQrOWV448Hyqw6eM58pYgMLEA2b8ePjYMPtsR+9I029rrM1iCn63CbaoazDf2sia6/L+NMLFeiL1yFoLTzdrz824bawxTzkhVPkYElH6au6uhklNOH/pwbykrjvrEx3MAveCpACW3fa3VoCokQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('dae141f7309e6a566027761d2ee713e4')


# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    elif  '陳威' in msg:
        message=TextSendMessage(text='yyds')
        line_bot_api.reply_message(event.reply_token, message)
    elif  '功能' in msg:
        message=TextSendMessage(text='最新合作廠商\n最新活動訊息\n註冊會員\n旋轉木馬\n圖片畫廊')
        line_bot_api.reply_message(event.reply_token, message)
    elif '早安' in msg:
        message=TextSendMessage(text=f'早安ㄚ 寶寶今天也很想你喔ฅ●ω●ฅ')
        line_bot_api.reply_message(event.reply_token, message)
    elif '早餐' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '河內塔' in msg:
        message=TextSendMessage(text=f'河內塔Java版<3\nhttps://github.com/tsaiiuo/HanoiStack_java')
        line_bot_api.reply_message(event.reply_token, message)
    elif '還沒' in msg:
        message = TextSendMessage(text='現在 立刻 馬上(／‵Д′)／~ ╧╧')
        line_bot_api.reply_message(event.reply_token, message)
    elif '有' in msg:
        message = LocationSendMessage(title: "臺北車站",
        address: "台灣台北市中正區北平西路3號100臺灣",latitude: 25.047702,
        longitude: 121.517373)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
