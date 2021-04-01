import sqlite3
from db import db 

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    pages = db.Column(db.Float(precision=1))
    
    store_id = db.Column(db.Integer, db.ForeignKey('lists.id'))


    def __init__(self, name, pages, lists_id):
        self.name = name
        self.pages = pages
        self.lists_id = lists_id


    def json(self):
        return {'name': self.name, 'price': self.pages}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

