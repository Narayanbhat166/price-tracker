from main import db

main_item1 = db.Table('main_item1',
                      db.Column('main_id', db.Integer, db.ForeignKey(
                          'main.id'), primary_key=True),
                      db.Column('item1_id', db.Integer, db.ForeignKey(
                          'item1.id'), primary_key=True))

main_item2 = db.Table('main_item2',
                      db.Column('main_id', db.Integer, db.ForeignKey(
                          'main.id'), primary_key=True),
                      db.Column('item2_id', db.Integer, db.ForeignKey(
                          'item2.id'), primary_key=True))


class Main(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item1 = db.relationship('Item1', secondary=main_item1,
                            backref=db.backref('mainitem'))
    item2 = db.relationship('Item2', secondary=main_item2,
                            backref=db.backref('mainitem'))


class Item1(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Item2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
