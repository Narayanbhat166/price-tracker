from main import db

user_flipkart = db.Table('user_flipkart',
                         db.Column('user_id', db.Integer, db.ForeignKey(
                             'user.id'), primary_key=True),
                         db.Column('flipkart_id', db.Integer, db.ForeignKey(
                             'flipkart.id'), primary_key=True))

user_amazon = db.Table('user_amazon',
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           'user.id'), primary_key=True),
                       db.Column('amazon_id', db.Integer, db.ForeignKey(
                           'amazon.id'), primary_key=True))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    chatid = db.Column(db.String(10), unique=True, nullable=False)
    flipkart_products = db.relationship(
        'Flipkart', secondary=user_flipkart, backref=db.backref('user'))
    amazon_products = db.relationship(
        'Amazon', secondary=user_amazon, backref=db.backref('user'))


class Flipkart(db.Model):
    __tablename__ = 'flipkart'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(500))
    url = db.Column(db.String(300), unique=True)
    price = db.Column(db.BigInteger)
    display_price = db.Column(db.String(20))
    stars = db.Column(db.Float)
    ratings = db.Column(db.BigInteger)
    reviews = db.Column(db.BigInteger)
    image_url = db.Column(db.String(300))
    updates = db.Column(db.String(1000))


class Amazon(db.Model):
    __tablename__ = 'amazon'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(500))
    url = db.Column(db.String(300), unique=True)
    price = db.Column(db.BigInteger)
    display_price = db.Column(db.String(20))
    stars = db.Column(db.Float)
    ratings = db.Column(db.BigInteger)
    reviews = db.Column(db.BigInteger)
    image_url = db.Column(db.String(300))
    updates = db.Column(db.String(1000))
