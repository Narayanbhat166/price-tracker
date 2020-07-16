import requests
from main import db
from models import User


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

        user = db.Query

        message_url = self.bot_url+'sendMessage'
        r = requests.post(message_url, json=json_data)

    def handle_request(self, data):
        self.chat_id = data['message']['chat']['id']
        self.sender = data['message']['from']['first_name']

        if User.query.filter_by(chatid=str(self.chat_id)).count() == 1:
            self.reply("You are already in the database")
        else:
            user = User(name=self.sender, chatid=str(self.chat_id))
            db.session.add(user)
            db.session.commit()
            self.reply("Added you into the database")

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
