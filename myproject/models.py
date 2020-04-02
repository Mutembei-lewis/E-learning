from myproject import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader

def load_user(user_id):

    return User.query.get(user_id)

class User(UserMixin, db.Model):

        __tablename__ = 'users'


        id = db.Column(db.Integer,primary_key = True)
        username = db.Column(db.String(64), unique= True)
        email = db.Column(db.String(64), unique = True,index =True)
        password_hash = db.Column(db.String(128))

        def get_reset_token(self,expires_sec = 1800):
                s=  Serializer(app.config['SECRET_KEY'],expires_sec)
                return s.dumps({'user_id': self.id}).decode('utf-8')
        
        
        @staticmethod
        def verify_reset_token(token):
            s= Serializer(app.config['SECRET_KEY'])
            try:
                user_id = s.loads(token)['user_id']
            except:
                return None
            return User.query.get(user_id)







        def __init__(self,email,username,password ):
            self.username = username
            self.email = email
            self.password_hash = generate_password_hash(password)

        def check_password(self,password):
            return check_password_hash(self.password_hash,password )



