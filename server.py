from flask import Flask, request
import requests

app = Flask(__name__)

bot_url = 'https://api.telegram.org/bot1291011387:AAEDG2wqE0t4XHbe_9RurkcJHJ_Fdw99rf8/'
web_hook = 'https://price-tracker-bot.herokuapp.com/'


def set_webhook():
    method = 'setWebHook' + '?url=https://{}'.format(web_hook)
    response = requests.get(bot_url + method)


class Telegram:
    def __init__(self):
        self.chat_id = ''
        self.sender = ''
        self.text = ''
        self.bot_url = 'https://api.telegram.org/bot1291011387:AAEDG2wqE0t4XHbe_9RurkcJHJ_Fdw99rf8/'

    def reply(self, message):
        json_data = {
            "chat_id": self.chat_id,
            "text": message
        }

        message_url = bot_url+'sendMessage'
        requests.post(message_url, json=json_data)

    def handle_request(self, data):
        self.chat_id = data['message']['chat']['id']
        self.sender = data['message']['from']['first_name']

        print(self.sender)

        if data.get('message').get('text') is not None:
            print("Text")
            self.text = data.get('message').get('text')
            self.reply(self.text)

        else:
            self.reply("Only Text")


@app.route('/')
def main():
    data = request.get_json()
    return "App running"


if __name__ == '__main__':
    telegram = Telegram()
    set_webhook()
    print("App running")

    app.run(debug=True, host='0.0.0.0')
