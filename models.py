from main import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    chatid = db.Column(db.String(10), unique=True, nullable=False)
    flipkart_products = db.relationship('Flipkart', backref='user')
    amazon_products = db.relationship('Amazon', backref='user')


class Flipkart(db.Model):
    __tablename__ = 'flipkart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(300), unique=True)
    price = db.Column(db.BigInteger)
    display_price = db.Column(db.String(20))
    stars = db.Column(db.Float)
    ratings = db.Column(db.BigInteger)
    reviews = db.Column(db.BigInteger)
    updates = db.Column(db.String(1000))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))


class Amazon(db.Model):
    __tablename__ = 'amazon'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(300), unique=True)
    price = db.Column(db.BigInteger)
    display_price = db.Column(db.String(20))
    stars = db.Column(db.Float)
    ratings = db.Column(db.BigInteger)
    reviews = db.Column(db.BigInteger)
    updates = db.Column(db.String(1000))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
