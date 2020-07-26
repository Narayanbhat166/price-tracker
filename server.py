from flask import request, jsonify
from Telegram import Telegram
from main import app, db
import requests


@app.route('/', methods=['POST'])
def post_route():
    data = request.get_json()
    telegram.handle_request(data)
    resp = jsonify(success=True)
    return resp


@app.route('/', methods=['GET'])
def get_route():
    return "<h1> App is running </h1>"


@app.route('/reset', methods=['GET'])
def create_db():
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()

    return "<h1> DB Recreated</h1>"


telegram = Telegram()


if __name__ == '__main__':
    telegram.set_webhook()
    print("App running")

    app.run(debug=True)
