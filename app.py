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


def record_order(product_id, amount_paid):
    """Adds the order details to the ORDER_DB file"""
    order_id = str(uuid.uuid4()).split('-', 1)[0]
    orders = {
        order_id: {
            'product_id': product_id,
            'amount_paid': amount_paid,
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
        amount_paid = float(form_dict['paid'])
        if PRODUCTS[product]['price'] >= amount_paid:
            flash('Order not placed - insufficient payment', 'danger')
        else:
            current_order_id = record_order(product, amount_paid)
            flash('Order Placed Successfully', 'success')
            return redirect(url_for('confirmation',order_id = current_order_id))
    return render_template('index.jinja', products=PRODUCTS, title='Order Form', **context)


@app.route('/confirmation/<order_id>/')
def confirmation(order_id):
    with open(ORDER_DB) as f:
        orders = yaml.safe_load(f) or {}

    order = orders.get(order_id)
    if order is None:
        flash('No order id found - please try again', 'danger')
    
    amount_paid = order['amount_paid']
    item_price = PRODUCTS[order['product_id']]['price']
    change_due = round(amount_paid - item_price,2)
    change_pence = int(change_due * 100)
    denom_string = ''
    for denom in DENOMINATIONS:
        num, change_pence = divmod(change_pence,denom['value'])
        if num > 0:
            denom_string += f'{denom["name"]}: {str(num)} '   
    return render_template('confirmation.jinja', order_id=order_id, amount_paid=amount_paid, item_price=item_price, change_due=change_due, denomination_str=denom_string, title='Order Confirmation')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
