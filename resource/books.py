import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.books import BookModel



class Book(Resource): # will this be the BookModel? it originally was the MT_Bookshelf
    parser = reqparse.RequestParser()
    parser.add_argument('pages',
    type=float,
    required=True,
    help="This field is blank... whoops."
    )
    parser.add_argument('lists_id',
    type=str,
    required=True,
    help="Store ID please."
    )
    
    @jwt_required()
    def get(self, name):
        book = BookModel.find_by_name(name)  
        if book:
            return book.json()
        return {"message": 'Book not found'}, 200 if book else 404

    def post(self, name):
        if BookModel.find_by_name(name):
                    return {"Message": "A book with the name '{}' already exists.".format(name)}, 400

        data = Book.parser.parse_args()

        book = BookModel(name, **data)
        
        try:
            book.save_to_db()
        except:
            return {"message": "An error has eccurred inserting the book."}, 500
        return book.json(), 201


    def delete(self, name):
        book = BookModel.find_by_name(name)
        if book:
            book.delete_from_db()

        return {'message': 'Book Deleted.'}

    def put(self, name):
        data = Book.parse.parse_args()

        book = BookModel.find_by_name(name)
        
        if book is None:
            book = BookModel.find_by_name(name)
        else:
            book.pages = data['pages']

        book.save_to_db()

        return book.json()
      

class BookList(Resource):
    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}