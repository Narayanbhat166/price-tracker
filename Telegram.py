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

    def reply(self, message):
        json_data = {
            "chat_id": self.chat_id,
            "text": message
        }

        message_url = self.bot_url+'sendMessage'
        r = requests.post(message_url, json=json_data)

    def send_photo(self, url, caption):
        json_data = {
            "chat_id": self.chat_id,
            "photo": url,
            "caption": caption
        }

        message_url = self.bot_url+'sendPhoto'
        r = requests.post(message_url, json=json_data)

    def handle_request(self, data):
        # print(data)
        self.chat_id = data['message']['chat']['id']
        self.sender = data['message']['from']['first_name']
        self.text = data['message'].get('text')

        if User.query.filter_by(chatid=str(self.chat_id)).count() == 1:
            print("You are already in the database")
        else:
            user = User(name=self.sender, chatid=str(self.chat_id))
            db.session.add(user)
            db.session.commit()
            print("Added you into the database")

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
            # self.reply("product from amazon")
            link = url.split('/')
            product_id = link[link.index('dp')+1]

            exists = Amazon.query.filter_by(product_id=product_id).first()

            if exists is None:
                print("Prduct is new")
                # get product from the internet
                product = amazon(product_id)

                title = product['title']
                price = product['price']
                display_price = product['display_price']
                ratings = product['ratings']
                reviews = product['reviews']
                stars = product['stars']
                image_url = product['image_url']

                self.send_photo(
                    image_url, "This is the one you told me to track!")

                message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                self.reply(message)

                # insert into database
                try:
                    product = Amazon(product_id=product_id,
                                     title=title, url=url, price=price, ratings=ratings, reviews=reviews, stars=stars, display_price=display_price, image_url=image_url)
                    product.user.append(user)
                    user.amazon_products.append(product)
                    db.session.add(product)
                    db.session.commit()
                except Exception as e:
                    print(
                        f"Exception {str(e)} occured while inserting product {product_id} into database")
                else:
                    # added product successfully
                    self.reply("Added product into the database")
                    print("Added product into the database")
                    products_from_amazon = Amazon.query.filter(
                        Amazon.user.contains(user))
                    products_from_flipkart = Flipkart.query.filter(
                        Flipkart.user.contains(user))
                message = f"You are currently tracking {products_from_amazon.count()} products from amazon and {products_from_flipkart.count()} products from flipkart. To list all the products use /list"
                self.reply(message)

            else:
                print("Product already exists in the database")
                self.reply("Someone else is already tracking this product!")

                # get product from the database
                # check if the same user is tracking the product

                products_from_amazon = Amazon.query.filter(
                    Amazon.user.contains(user)).all()

                product = exists

                if product in products_from_amazon:
                    self.reply(
                        "You are already tracking the product, asshole!")
                else:

                    product = exists

                    title = product.title
                    price = product.price
                    display_price = product.display_price.replace('?', '₹')
                    ratings = product.ratings
                    reviews = product.reviews
                    stars = product.stars
                    image_url = product.image_url

                    product.user.append(user)
                    db.session.commit()

                    self.send_photo(
                        image_url, "This is the one you told me to track!")

                    message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                    self.reply(message)

                    products_from_amazon = Amazon.query.filter(
                        Amazon.user.contains(user))
                    products_from_flipkart = Flipkart.query.filter(
                        Flipkart.user.contains(user))
                    message = f"You are currently tracking {products_from_amazon.count()} products from amazon and {products_from_flipkart.count()} products from flipkart. To list all the products use /list"
                    self.reply(message)

        elif 'flipkart' in url:
            self.reply("Product from Flipkart")
            link = url.split('?')
            product_id = link[1][4:20]

            exists = Flipkart.query.filter_by(product_id=product_id).first()

            if exists is None:
                print("Prduct is new")
                # get product from the internet
                product = flipkart(product_id)

                title = product['title']
                price = product['price']
                display_price = product['display_price']
                ratings = product['ratings']
                reviews = product['reviews']
                stars = product['stars']
                image_url = product['image_url']

                self.send_photo(
                    image_url, "This is the one you told me to track!")

                message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                self.reply(message)

                # insert into database
                try:
                    product = Flipkart(product_id=product_id,
                                       title=title, url=url, price=price, ratings=ratings, reviews=reviews, stars=stars, display_price=display_price, image_url=image_url)
                    product.user.append(user)
                    user.flipkart_products.append(product)
                    db.session.add(product)
                    db.session.commit()
                except Exception as e:
                    print(
                        f"Exception {str(e)} occured while inserting product {product_id} into database")
                else:
                    # added product successfully
                    self.reply("Added product into the database")
                    print("Added product into the database")
                    products_from_amazon = Amazon.query.filter(
                        Amazon.user.contains(user))
                    products_from_flipkart = Flipkart.query.filter(
                        Flipkart.user.contains(user))
                    message = f"You are currently tracking {products_from_amazon.count()} products from amazon and {products_from_flipkart.count()} products from flipkart. To list all the products use /list"
                    self.reply(message)

            else:
                print("Product already exists in the database")
                self.reply("Someone else is already tracking this product!")
                # get product from the database
                # check if the same user is trying to track the product again, Damn user!

                products_from_flipkart = Flipkart.query.filter(
                    Flipkart.user.contains(user)).all()

                product = exists

                if product in products_from_flipkart:
                    self.reply(
                        "You are already tracking the product, asshole!")
                else:

                    title = product.title
                    price = product.price
                    display_price = product.display_price.replace('?', '₹')
                    ratings = product.ratings
                    reviews = product.reviews
                    stars = product.stars
                    image_url = product.image_url

                    # Add user to the product
                    product.user.append(user)
                    db.session.commit()

                    self.send_photo(
                        image_url, "This is the one you told me to track!")

                    message = f"Title: {title}\n\nPrice: {display_price}\n\nRated by: {ratings} Customers\n\nReviewed by: {reviews} Customers\n\nStars: {stars}\n\n\nYou will be updated about the product information whenever the price changes or everyday at a particular time"
                    self.reply(message)

                    products_from_amazon = Amazon.query.filter(
                        Amazon.user.contains(user))
                    products_from_flipkart = Flipkart.query.filter(
                        Flipkart.user.contains(user))
                    message = f"You are currently tracking {products_from_amazon.count()} products from amazon and {products_from_flipkart.count()} products from flipkart. To list all the products use /list"
                    self.reply(message)

        else:
            self.reply("Product not recognized")

    def handle_commands(self, command):
        command = command[1:]

        if command == 'list':
            user = User.query.filter_by(chatid=self.chat_id).first()
            products_from_amazon = Amazon.query.filter(
                Amazon.user.contains(user))
            products_from_flipkart = Flipkart.query.filter(
                Flipkart.user.contains(user))
            message = ''

            if products_from_amazon.count() == 0:
                message = "No products tracked from Amazon\n\n"

            if products_from_flipkart.count() == 0:
                message = "No products tracked from Flipkart"

            if products_from_flipkart.count() > 0:
                message += f'Tracking {products_from_flipkart.count()} Products from flipkart\n\n'

                for product in products_from_flipkart.all():
                    price = product.display_price.replace('?', '₹')
                    message += f'Title: {product.title}\nPrice: {price}\n\n'

                message += "\n\n"

            if products_from_amazon.count() > 0:
                message += f'Tracking {products_from_amazon.count()} Products from Amazon\n\n'

                for product in products_from_amazon.all():
                    price = product.display_price.replace('?', '₹')
                    message += f'Title: {product.title}\nPrice: {price}\n\n'

            self.reply(message)

        if command == 'start':
            # send a welcome message and images
            message = "Checking for your products frequently if there is a fall in price? Leave it to me. Share the link to the product which you want me to track, and i will be at your mercy"

            self.reply(message)

            self.send_photo('AgACAgUAAxkBAAIKDV8eY63HjpgcxHOZrnkZzYyWZbVXAAJBqjEbjfXxVD1y3wLyfl_VPN--anQAAwEAAwIAA3gAA0L2BQABGgQ',
                            "As simple as this, Give it a try!")

    def set_webhook(self, web_hook):
        method = 'deleteWebHook'
        r = requests.get(self.bot_url + method)
        print(r.json())
        if r.status_code == 200:
            method = 'setWebHook' + '?url={0}'.format(web_hook)
            r = requests.get(self.bot_url + method)
            print(r.url)
            print(r.json())
            if r.status_code == 200:
                print("set webhook")
