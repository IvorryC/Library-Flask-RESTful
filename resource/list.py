from flask_restful import Resource
from models.list import ListModel

class List(Resource):
    def get (self,name):
        list = ListModel.find_by_name(name)
        if list:
            return list.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if ListModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        list = ListModel(name)
        try:
            list.save_to_db()
        except:
            return {'message': 'An error occurred while creating the list.'}, 500  

        return list.json(), 201

    def delete(self, name):
        list = ListModel.find_by_name(name)
        if list:
            list.delete_from_db()

        return {'message': 'Store deleted.'}


class ListList(Resource):
    def get(self):
        return {'lists': [list.json() for list in ListModel.query.all()]}
