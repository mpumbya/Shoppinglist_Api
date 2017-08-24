from app import bcrypt, db
import jwt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True)
    password = db.Column(db.String(255))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return user.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<user: {}>".format(self.username)
        
    def encode_auth_token(self,id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,second=5),
                'iat': datetime.datetime.utcnow(),
                'sub': id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm ='H256'
            )
        except Exception as e:
            return e

class List(db.Model):
    __tablename__ = 'lists'
    list_Id = db.Column(db.Integer, primary_key=True)
    user_Id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return list.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<list: {}>".format(self.name)


class Item(db.Model):
    __tablename__ = 'items'
    item_Id = db.Column(db.Integer, primary_key=True)
    list_Id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return item.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<item: {}>".format(self.name)
