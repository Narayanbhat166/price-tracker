from main.amazon import amazon
from main import db
from models import Amazon, User
import datetime
import requests
import pytz


bot_url = 'https://api.telegram.org/bot1291011387:AAEDG2wqE0t4XHbe_9RurkcJHJ_Fdw99rf8/'


def reply(message, chat_id):
    global bot_url
    json_data = {
        "chat_id": chat_id,
        "text": message
    }

    message_url = bot_url+'sendMessage'
    r = requests.post(message_url, json=json_data)


def update_amazon(product_id):
    new_details = amazon(product_id)

    old_details = Amazon.query.filter_by(product_id=product_id).first()

    message = new_details['title']+'\n\n'
    updates = False

    if new_details['price'] != old_details.price:
        updates = True
        diff = new_details['price'] - old_details.price
        if diff > 0:
            message += "Price Increased by "+str(diff)+"\n\n"
        else:
            message += "Price Decreased by "+str(diff)+"\n\n"

        old_details.price = new_details['price']
        db.session.commit()

    if new_details['ratings'] != old_details.ratings:
        updates = True
        diff = new_details['ratings'] - old_details.ratings
        message += str(diff)+" New ratings\n\n"

        old_details.ratings = new_details['ratings']
        old_details.reviews = new_details['reviews']
        db.session.commit()

    if new_details['stars'] != old_details.stars:
        updates = True
        diff = new_details['stars'] - old_details.stars
        message += str(diff)+" Increase in star rating\n\n"

        old_details.stars = new_details['stars']
        db.session.commit()

    if updates:
        print(message)
        old_details.updates = message

        # send the message to everyone subscribed
        user = User.query.filter_by(id=old_details.owner).first()
        reply(message, user.chatid)

        db.session.commit()
        return message
    else:
        print("No updates, last checked ", datetime.datetime.now(
            tz=pytz.timezone('Asia/Kolkata')))

    db.session.commit()
