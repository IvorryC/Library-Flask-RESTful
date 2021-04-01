from flask import Flask 
from flask_restful import Api 
from flask_jwt import JWT
# its an API now
from security import authenticate, identity
from resource.users import UserRegister 
from resource.books import Book, BookList 
from resource.list import List, ListModel, ListList
from db import db 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'splite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'DontTestMe'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # Auth

api.add_resource(Book, '/book/<string:name>')
api.add_resource(List, '/list/<string:name>')
api.add_resource(BookList, '/books')
api.add_resource(ListList, '/lists')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)