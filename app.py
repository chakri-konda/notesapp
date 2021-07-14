from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from crypt import encrypted, decrypted

app = Flask(__name__)

usrname = "root"
pswd = "Root#123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@localhost/workindia'.format(usrname, pswd)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), primary_key=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_notes = relationship('Notes', backref='users')

    def __init__(self, username, password):
        self.username = username
        self.password = encrypted(password)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def info(self):
        return {
            "id": self.userid,
            "username": self.username,
            "password": self.password
        }


class Notes(db.Model):
    __tablename__ = 'notes'

    id = db.Column('userId', db.Integer, primary_key=True)

    note = db.Column('note', db.String(10000), primary_key=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    

    
    def __init__(self, userid, note):
        self.userid = userid
        self.note = encrypted(note)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def usernote(self):
        return decrypted(self.note)
    
    def __repr__(self):
        return f'<Notes: {self.userid} {decrypted(self.note)}>'
    


@app.route('/<int:id>', methods=['GET', 'POST'])
def start(id):

    return jsonify({
        "status": "connected"
    })


@app.route('/app/user', methods=['POST'])
def register():

    body = request.get_json()
    try:
        username = body.get('username', None)
        password = body.get('password', None)

        user = Users(username=username, password=password)
        Users.insert(user)
        return jsonify({
            "status": "account created"
        })

    except Exception as e:
        print(e)
    return({
        "status": "Internal Error"
    }, 500)

@app.route('/app/user/auth', methods=['POST'])
def login():
    body = request.get_json()

    try:
        username = body.get('username', None)
        password = body.get('password', None)

        user = Users.query.filter_by(username=username).first()

        if decrypted(user.info()['password']) == password:
            return jsonify({
                "status": "success",
                "userId": user.userid
            })
        else:
            return jsonify({
                "status": "wrong password"
            })

    except Exception as e:
        print("Exception", e)
    return({
        "status": "Internal Error"
    }, 500)

@app.route('/app/sites/list/<int:id>', methods=['GET', 'POST'])
def list_notes(id):
    try:
        notes_query = Notes.query.filter(Notes.userid==id).all()
        notes_data = list(map(Notes.usernote, notes_query))

        if (len(notes_data) == 0):
            return({
                "status": "no records found"
            })
        return jsonify({
            "id": id,
            'notes': notes_data
        })

    except Exception as e:
        print(e)
    return({
        "status": "Internal Error"
    }, 500)

@app.route('/app/sites/<int:id>', methods=['GET', 'POST'])
def save_note(id):
    body = request.get_json()

    try:
        note = body.get('note', None)
        user_note = Notes(userid=id, note=note)
        Notes.insert(user_note)

        return jsonify({
            "status": "success"
        })

    except Exception as e:
        print(e)
    return({
        "status": "Internal Error"
    }, 500)


if __name__ == "__main__":
    app.run()