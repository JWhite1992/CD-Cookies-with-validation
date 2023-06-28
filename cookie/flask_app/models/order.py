from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Order:
    db = "cookie_stand"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.number = data['number']

    @classmethod
    def bake_it(cls, data):
        query ="INSERT INTO orders (name, cookie_type, number) VALUES (%(name)s, %(cookie_type)s, %(number)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query ="SELECT * FROM orders;"
        all_orders = connectToMySQL(cls.db).query_db(query)
        return all_orders

    @classmethod
    def get_cookie(cls, order_id):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        peppermint = {
            'id': order_id
        }
        one_cookie = connectToMySQL(cls.db).query_db(query, peppermint)  
        order_data = one_cookie[0]
        order = {
            'id': order_data['id'],
            'name': order_data['name'],
            'cookie_type': order_data['cookie_type'],
            'number': order_data['number']
        }
        return order


    @classmethod
    def rebake(cls, order_id, data):
        query = f"UPDATE orders SET name = %(name)s, cookie_type = %(cookie_type)s, number = %(number)s WHERE id = %(id)s;"
        data['id'] = order_id
        return connectToMySQL(cls.db).query_db(query, data)
        
    @staticmethod
    def validate_cookie_order(orders):
        is_valid=True
        if len(orders['name'])< 3:
            flash('Name is not long enough needs to be longer than 3 letters')
            is_valid= False
        if len(orders['cookie_type']) < 3:
            flash('Cookie Type is not long enough needs to be longer than 4 letters')
            is_valid= False
        if len(orders['number']) < 1:
            flash('Number is invalid must order at least one')
            is_valid= False
        return is_valid