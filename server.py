from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


class Telegram:
    def __init__(self):
        self.chat_id = ''
        self.sender = ''
        self.text = ''
        self.bot_url = 'https://api.telegram.org/bot1291011387:AAEDG2wqE0t4XHbe_9RurkcJHJ_Fdw99rf8/'
        self.web_hook = 'https://price-tracker-bot.herokuapp.com/'

    def reply(self, message):
        json_data = {
            "chat_id": self.chat_id,
            "text": message
        }

        message_url = self.bot_url+'sendMessage'
        r = requests.post(message_url, json=json_data)
        print(r.url)
        print(r.status_code)

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

    def set_webhook(self):
        method = 'deleteWebHook'
        r = requests.get(self.bot_url + method)
        print(r.json())
        if r.status_code == 200:
            method = 'setWebHook' + '?url={0}'.format(self.web_hook)
            r = requests.get(self.bot_url + method)
            print(r.url)
            print(r.json())
            if r.status_code == 200:
                print("set webhook")


@app.route('/', methods=['POST'])
def post_route():
    data = request.get_json()
    telegram.handle_request(data)
    resp = jsonify(success=True)
    return resp


@app.route('/', methods=['GET'])
def get_route():
    return "<h1> App is running </h1>"


telegram = Telegram()


if __name__ == '__main__':
    telegram.set_webhook()
    print("App running")

    app.run(debug=True)
