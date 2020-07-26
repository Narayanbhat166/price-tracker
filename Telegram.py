import requests
from main import db
from models import User, Flipkart, Amazon
from main.amazon import amazon
from main.flipkart import flipkart


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

    def send_photo(self, url):
        json_data = {
            "chat_id": self.chat_id,
            "photo": url
        }

        message_url = self.bot_url+'sendPhoto'
        r = requests.post(message_url, json=json_data)

    def handle_request(self, data):
        # print(data)
        self.chat_id = data['message']['chat']['id']
        self.sender = data['message']['from']['first_name']
        self.text = data['message'].get('text')

        if User.query.filter_by(chatid=str(self.chat_id)).count() == 1:
            self.reply("You are already in the database")
        else:
            user = User(name=self.sender, chatid=str(self.chat_id))
            db.session.add(user)
            db.session.commit()
            self.reply("Added you into the database")

        if data["message"].get("entities") is not None:
            # print(data["message"].get("entities")[0].get('type'))
            if data["message"].get("entities")[0].get('type') == "url":
                self.handle_url(self.text)

            if data["message"].get("entities")[0].get('type') == "bot_command":
                self.handle_commands(self.text)

        elif self.text is not None:
            self.text = data.get('message').get('text')
            self.reply(self.text)

        else:
            self.reply("I acccept Only Text")

    def handle_url(self, url_text):
        url = url_text[url_text.index('http'):]
        title = url_text[:url_text.index('http')]

        user = User.query.filter_by(chatid=str(self.chat_id)).first()

        #print(url, title, user.name)

        if 'amazon' in url:
            self.reply("product from amazon")
            link = url.split('/')
            product_id = link[link.index('dp')+1]

            exists = Amazon.query.filter_by(product_id=product_id).first()

            if exists is None:
                print("Prduct is new")
                # get details from the internet
                details = amazon(product_id)

                title = details['title']
                price = details['price']
                display_price = details['display_price']
                ratings = details['ratings']
                reviews = details['reviews']
                stars = details['stars']
                image_url = details['image_url']

                self.send_photo(image_url)

                message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                self.reply(message)

                # insert into database
                try:
                    product = Amazon(product_id=product_id,
                                     title=title, url=url, owner=user.id, price=price, ratings=ratings, reviews=reviews, stars=stars, display_price=display_price)
                    db.session.add(product)
                    db.session.commit()
                except Exception as e:
                    print(
                        f"Exception {str(e)} occured while inserting product {product_id} into database")
                else:
                    # added product successfully
                    self.reply("Added product into the database")
                    print("Added product into the database")

            else:
                print("Product already exists in the database")
                self.reply("Someone else is already tracking this product!")
                # get details from the database

                details = Amazon.query.filter_by(product_id=product_id).first()

                title = details.title
                price = details.price
                display_price = details.display_price.replace('?', '₹')
                ratings = details.ratings
                reviews = details.reviews
                stars = details.stars
                image_url = details.image_url

                self.send_photo(image_url)

                message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                self.reply(message)

                products_from_amazon = Amazon.query.filter_by(user=user)
                products_from_flipkart = Flipkart.query.filter_by(user=user)
                message = f"You are currently tracking {products_from_amazon.count()} products from amazon and {products_from_flipkart.count()} products from flipkart. To list all the products use /list"
                self.reply(message)

        elif 'flipkart' in url:
            self.reply("Product from Flipkart")
            link = url.split('?')
            product_id = link[1][4:20]

            exists = Flipkart.query.filter_by(product_id=product_id).first()

            if exists is None:
                print("Prduct is new")
                # get details from the internet
                details = flipkart(product_id)

                title = details['title']
                price = details['price']
                display_price = details['display_price']
                ratings = details['ratings']
                reviews = details['reviews']
                stars = details['stars']
                image_url = details['image_url']

                self.send_photo(image_url)

                message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                self.reply(message)

                # insert into database
                try:
                    product = Flipkart(product_id=product_id,
                                       title=title, url=url, owner=user.id, price=price, ratings=ratings, reviews=reviews, stars=stars, display_price=display_price)
                    db.session.add(product)
                    db.session.commit()
                except Exception as e:
                    print(
                        f"Exception {str(e)} occured while inserting product {product_id} into database")
                else:
                    # added product successfully
                    self.reply("Added product into the database")
                    print("Added product into the database")

            else:
                print("Product already exists in the database")
                self.reply("Someone else is already tracking this product!")
                # get details from the database

                details = Flipkart.query.filter_by(
                    product_id=product_id).first()

                title = details.title
                price = details.price
                display_price = details.display_price.replace('?', '₹')
                ratings = details.ratings
                reviews = details.reviews
                stars = details.stars
                image_url = details.image_url

                self.send_photo(image_url)

                message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                self.reply(message)

        else:
            self.reply("Product not recognized")

    def handle_commands(self, command):
        command = command[1:]

        if command == 'list':
            user = User.query.filter_by(chatid=self.chat_id).first()
            products_from_amazon = Amazon.query.filter_by(user=user)
            products_from_flipkart = Flipkart.query.filter_by(user=user)

            if products_from_flipkart.count() > 0:
                message = f'Tracking {products_from_flipkart.count()} Products from flipkart\n\n'

                for product in products_from_flipkart:
                    price = product.display_price.replace('?', '₹')
                    message += f'Title: {product.title}\nPrice: {price}\n\n'

                message += "\n\n"

            if products_from_amazon.count() > 0:
                message += f'Tracking {products_from_amazon.count()} Products from Amazon\n\n'

                for product in products_from_amazon:
                    price = product.display_price.replace('?', '₹')
                    message += f'Title: {product.title}\nPrice: {price}\n\n'

            if products_from_amazon.count() == 0:
                message += "No products tracked from Amazon"

            if products_from_flipkart.count() == 0:
                message += "No products tracked from Flipkart"

            self.reply(message)

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
