from flask import Flask, request, abort, render_template
from Image_boot_cls import image_boot_cls
from Servo import servo_run
from ping import ping_host
import time

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('8O0fX4TyHDlvt9wAWbP3jeVmLufH6KksuIxlAu9vI3FjkMJfoE0mqsQ7PjcxwUU2Ppc2S/7TaJcRUFWGvTtqUlEZmrftmkhnkw5xZdZn5nhLijDb0lRQeSGKQMZs6M24p/nP3mdc+I9aa1FD68MPPwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5d92af10fe73a416f9cc0c1c0d5e62c0')
 

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    # 
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    if event.message.text == '有開機嗎': # 

       boot_variable = image_boot_cls() 
       if boot_variable == 1: # which is computer off
            c_state = 'Off'
       else: # which is computer on
            c_state = 'On'
       print('[Boot_variable]:',boot_variable)
       if c_state =='Off':
           text = '報告~沒開機!!'
       else:
           text = '報告~有開機!!'  
       line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=text))
       
    elif event.message.text == '幫我開機':
        
       # Arm moving
       time.sleep(5)
       servo_run()
       success_move_arm_text='手臂狀態: 成功'
       
       
       # Check is boost or not
       boot_variable = image_boot_cls() 
       if boot_variable == 1: # which is computer off
            c_state = 'Off'
       else: # which is computer on
            c_state = 'On'
       print('[Boot_variable]:',boot_variable)
       time.sleep(2)
       if c_state =='Off':
           boost_text = '電腦狀態: 關機'
       else:
           boost_text = '電腦狀態: 開機'
    
       # Check Network
       response = ping_host()
       if response==0:
           network_text = '網路狀態: 成功'
       else:
           network_text = '網路狀態: 失敗'
           
       all_text = '[通知]\n'+success_move_arm_text+'\n'+boost_text+'\n'+network_text
       
       # Give advice
       if c_state =='Off' and response == 0:
           advice_text = '電腦電源可能沒開'
       elif  c_state =='Off' and response == 1:
           advice_text = '電腦電源可能沒開且沒有網路'
       elif  c_state =='On' and response == 1: 
           advice_text = '已成功開啟電腦但沒有網路'
       else:
           advice_text = '您可以遠端電腦了'
       
       all_advice = '[診斷電腦]\n'+advice_text
       
       line_bot_api.reply_message(
       event.reply_token,
       [TextSendMessage(text=all_text),TextSendMessage(text=all_advice)])     
       
    elif event.message.text == '幫我關機':
        
       move_complete_text = '目前功能無法關機...'
       line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=move_complete_text))
       
    elif event.message.text == '你好' or event.message.text == '安安':
        text = 'Hello~'
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text))
        
        
    else: # 
        Not_know_text= '我聽不懂你的意思'
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=Not_know_text))

if __name__ == "__main__":
    app.run()



