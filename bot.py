import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# Set LINE Messaging API credentials
channel_access_tokens = {
    'oa1': 'ZC0GUdLKLxZQN9p2AeDCTMeM8nS+PfDhxGUY8tLYLvaOavE/8FxpxCZ0yPgpnj0FwPj6gMUfwXlU0MbUEMGeH9w/SuDLeILUypZPnPBwJ9QeTv4ThDZpZecJObAMwFJRHCD4pwbGqbjl5uZp995V7gdB04t89/1O/w1cDnyilFU=',
    'oa2': 'UIKgv34FeWZNmqaSZxd2oNU0H3SKTsJuSbRdXMPtEPmCYCT2IZIf0ND2CYxznbHul/pkhzPp57CO0rc9/WxyOcthbHAxSnaHAV8s3BVdjv/ktWF7l8nhGVDIW0e1soJF5SjKQJMWeauQrYGAmT/tIgdB04t89/1O/w1cDnyilFU=',
    # Add more OAs and their access tokens here
}

channel_secrets = {
    'oa1': '0dfdbcb7bf2b36edb1442ab4df30720a',
    'oa2': '7bf267acff743b5e864c894ac50a9250',
    # Add more OAs and their secrets here
}

line_bot_apis = {oa: LineBotApi(access_token) for oa, access_token in channel_access_tokens.items()}
handlers = {oa: WebhookHandler(channel_secret) for oa, channel_secret in channel_secrets.items()}

@app.route("/callback/<oa>", methods=['POST'])
def callback(oa):
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handlers[oa].handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handlers['oa1'].add(MessageEvent, message=TextMessage)
def handle_message_oa1(event):
    oa = 'oa1'

    # Check the inactive duration of the LINE OA (pseudo code)
    inactive_duration = get_inactive_duration(oa)
    if inactive_duration >= 1 * 60:  # 5 minutes in seconds
        # Send a response from the chatbot
        response = "Hello, this is the chatbot for OA1. How can I assist you?"
        line_bot_apis[oa].reply_message(event.reply_token, TextSendMessage(text=response))

@handlers['oa2'].add(MessageEvent, message=TextMessage)
def handle_message_oa2(event):
    oa = 'oa2'

    # Check the inactive duration of the LINE OA (pseudo code)
    inactive_duration = get_inactive_duration(oa)
    if inactive_duration >= 5 * 60:  # 5 minutes in seconds
        # Send a response from the chatbot
        response = "Hello, this is the chatbot for OA2. How can I assist you?"
        line_bot_apis[oa].reply_message(event.reply_token, TextSendMessage(text=response))

def get_inactive_duration(oa):
    # Fetch the last active timestamp for the LINE OA from a storage system
    # and calculate the inactive duration
    # Return the duration in seconds
    pass

if __name__ == "__main__":
    app.run()
