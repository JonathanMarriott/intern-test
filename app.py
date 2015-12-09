import uuid

import yaml
from flask import Flask, flash, request, render_template
app = Flask(__name__)
app.secret_key = 'life is pointless'

with open('products.yml') as _f:
    PRODUCTS = yaml.load(_f)

with open('denominations.yml') as _f:
    DENOMINATIONS = yaml.load(_f)


ORDER_DB = 'orders.yml'


def record_order(product_id):
    order_id = str(uuid.uuid4()).split('-', 1)[0]
    orders = {
        order_id: {
            'product_id': product_id,
        }
    }
    with open(ORDER_DB, 'a') as f:
        f.write(yaml.dump(orders, default_flow_style=False))


@app.route('/', methods=['POST', 'GET'])
def index():
    context = {}
    if request.method == 'POST':
        flash('Order Placed Successfully', 'success')
        # TODO
    return render_template('index.jinja', products=PRODUCTS, title='Order Form', **context)


@app.route('/confirmation/<order_id>')
def confirmation(order_id):
    with open(ORDER_DB) as f:
        orders = yaml.load(f) or {}

    order = orders.get(order_id)
    if order is None:
        pass  # TODO what do we do here?
    # TODO other stuff has to be calculated here.
    return render_template('confirmation.jinja', order_id=order_id, title='Order Confirmation')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
