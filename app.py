from itertools import product
import uuid
from flask.helpers import url_for
import yaml

from flask import Flask, flash, redirect, request, render_template

app = Flask(__name__)
app.secret_key = 'intern_test'
ORDER_DB = 'orders.yml'

with open('products.yml') as _f:
    PRODUCTS = yaml.safe_load(_f)

with open('denominations.yml') as _f:
    DENOMINATIONS = yaml.safe_load(_f)


def record_order(product_id):
    """Adds the order details to the ORDER_DB file"""
    order_id = str(uuid.uuid4()).split('-', 1)[0]
    orders = {
        order_id: {
            'product_id': product_id,
        }
    }
    with open(ORDER_DB, 'a') as f:
        f.write(yaml.dump(orders, default_flow_style=False))
    return order_id

@app.route('/', methods=['POST', 'GET'])
def index():
    context = {}
    if request.method == 'POST':
        # TODO: Validate and process the data entered in the form
        print('Form Submitted with data:', request.form)
        form_dict = request.form
        #Check amount paid is greater than price
        product = int(form_dict['product'])
        if PRODUCTS[product]['price'] > float(form_dict['paid']):
            print("Buyer did not pay enough")
            flash('Order not placed - insufficient payment', 'danger')
        else:
            current_order_id = record_order(product)
            flash('Order Placed Successfully', 'success')
            return redirect(url_for('confirmation',order_id = current_order_id))
    return render_template('index.jinja', products=PRODUCTS, title='Order Form', **context)


@app.route('/confirmation/<order_id>/')
def confirmation(order_id):
    with open(ORDER_DB) as f:
        orders = yaml.safe_load(f) or {}

    order = orders.get(order_id)
    if order is None:
        # TODO: What should we do here?
        pass

    # TODO: Get the context for the confirmation page
    return render_template('confirmation.jinja', order_id=order_id, title='Order Confirmation')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
