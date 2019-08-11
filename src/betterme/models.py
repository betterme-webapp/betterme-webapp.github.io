from betterme import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True) #id is added after being commited to a db
    username = db.Column(db.String(20), unique = True, nullable = False)  
    image_file = db.Column(db.String(20), nullable=False, default ='default.jpg')
    password = db.Column(db.String(60), nullable = False) 
    surveys = db.relationship ('Survey',backref = 'author', lazy = True)  
    
    def __repr__(self):
        return f"User('{self.username}','{self.image_file}')"

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key = True)  
    questionText = db.Column(db.String(1000), nullable = False)
    answerText = db.Column(db.Text, nullable = False)
    #the date is added after being commited to a db
    dateCompleted = db.Column(db.String(100), nullable = False, default = datetime.utcnow().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)

    def __repr__(self):
        return f"Survey('{self.questionText}','{self.answerText}','{self.dateCompleted}', and belongs to '{self.user_id}')"
