from flask import Flask, render_template, request, redirect, session
from flask_app.models.order import Order
from flask_app import app

@app.route('/')
def home():
    return redirect('/show/all')

@app.route('/show/all')
def show_all():
    orders = Order.get_all()
    return render_template("orders.html", orders=orders)

@app.route('/new/cookie/<int:order_id>', methods=['GET'])
def get_one_cookie(order_id):
    order = Order.get_cookie(order_id)
    return render_template('edit_order.html', order=order)

@app.route('/make/new/order')
def new_order():
    order = {
        'name' : ['name'],
        'cookie_type' : ['cookie_type'],
        'number' : ['number']
    }
    return render_template('create_order.html', order=order)

@app.route('/create/order', methods=['POST'])
def save_order():
    if not Order.validate_cookie_order(request.form):
        return redirect('/make/new/order')
    Order.bake_it(request.form)
    return redirect('/')

@app.route('/edit/order/<int:order_id>', methods=['GET'])
def edit_order(order_id):
    order = Order.get_cookie(order_id)
    print(order)
    return render_template('edit_order.html', order=order)

@app.route('/rebake/order/<int:order_id>', methods=['POST'])
def rebake(order_id):
    order_data = {
        'name': request.form['name'],
        'cookie_type': request.form['cookie_type'],
        'number': request.form['number']
    }
    Order.rebake(order_id, order_data)
    return redirect('/show/all')

