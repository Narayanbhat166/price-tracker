from main import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    chatid = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
