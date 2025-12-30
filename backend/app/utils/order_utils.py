import random
from flask import jsonify
from datetime import date
from app.models.models import Product,Customer
from uuid import uuid4


def generate_orders(req_date):
    payment_methods = [
        "Credit Card",
        "Bank Transfer",
        "Digital Wallet",
        "Cash on Delivery"
    ]
    provinces_iso = [
        "ID-JB",  # Jawa Barat
        "ID-JI",  # Jawa Timur
        "ID-JT",  # Jawa Tengah
        "ID-SU",  # Sumatera Utara
        "ID-BT",  # Banten
        "ID-JK",  # DKI Jakarta
        "ID-LA",  # Lampung
        "ID-SS",  # Sumatera Selatan
        "ID-SN",  # Sulawesi Selatan
        "ID-RI",  # Riau
        "ID-BA",  # Bali
        "ID-SB",  # Sumatera Barat
        "ID-KS",  # Kalimantan Selatan
        "ID-NB",  # Nusa Tenggara Barat
        "ID-AC"   # Aceh
    ]
    # order_statuses = [
    #     "Pending",
    #     "Processing",
    #     "Shipped",
    #     "Delivered", "Cancelled", "Returned", "Refunded"
    # ]
    sales_date = date.fromisoformat(req_date) if req_date else date.today()
    if(sales_date>date.today()):
        return jsonify({'error_msg':'date not valid'}),500
    n_order = random.randint(a=50,b=100)
    order_list = []
    products = Product.query.all()
    customers = Customer.query.all()
    for _ in range(0,n_order):
        n_item = random.randint(a=1,b=4)
        random_payment_method  = random.choice(payment_methods)
        random_customer = random.choice(customers)
        random_region = random.choice(provinces_iso[0:6] if random.randint(a=0,b=100)<=50 else provinces_iso[6:])

        item_list = []
        item_id_set = set()
        product_cost = 0

        for _ in range(0,n_item):
            
            random_item = random.choice(products).to_dict()
            if(random_item['id'] in item_id_set):
                continue

            random_item['qty']=random.randint(1,3 if random_item['product_price']>50 else 5)
            random_item['sub_total']=random_item['qty']*random_item['product_price']
            product_cost+=random_item['sub_total']
            item_list.append(random_item)
            item_id_set.add(random_item['id'])
        shipping_cost = random.randint(10,15 if product_cost>500 else 20) * product_cost/100
        
        order_list.append(
            {'order_id':f"ORDER_{uuid4()}",
            #  'order_status':"",
             'customer':random_customer.to_dict(),
             "shipping_region":random_region,
             "product_cost":product_cost,
             "shipping_cost":shipping_cost,
             "payment_method":random_payment_method,
             'items':item_list}
             )
    return order_list,sales_date