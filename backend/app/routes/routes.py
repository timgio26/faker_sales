from flask import Blueprint,request,jsonify
from app.models.models import Product,Customer
from app.extension import db
from uuid import UUID
from app.utils.order_utils import generate_orders

main_bp = Blueprint('main', __name__)

@main_bp.route('/version')
def version():
    return "0.0.1",200


# generate random 50-100 order
# date is optional default is today
@main_bp.get('/api/sales')
def get_sales():
    req_date = request.args.get('date')
    order_list,sales_date = generate_orders(req_date)
    return jsonify({'sales_date':sales_date.isoformat(),'order':order_list}),200

# get all product
@main_bp.get('/api/products')
def get_all_product():
    products = Product.query.all()
    return jsonify([i.to_dict() for i in products]),200

# add new product
@main_bp.post('/api/products')
def add_product():
    new_product = Product(**request.json)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added'}), 201

# delete one product
@main_bp.delete("/api/products/<id>")
def del_product(id):
    product = Product.query.get_or_404(UUID(id))
    print(product.product_name)
    db.session.delete(product)
    db.session.commit()
    return "",204  

# get all customers
@main_bp.get('/api/customers')
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([i.to_dict() for i in customers]),200

# add new customer
@main_bp.post('/api/customers')
def add_customer():
    new_customer = Customer(**request.json)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added'}), 201

# delete one customer
@main_bp.delete("/api/customers/<id>")
def del_customer(id):
    customer = Customer.query.get_or_404(UUID(id))
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'}),204  





