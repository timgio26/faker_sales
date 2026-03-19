import random
from flask import jsonify
from datetime import date,timedelta,datetime
from app.models.models import Product,Customer,Order,Order_Item
from uuid import uuid4,UUID
from app.extension import db


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
order_statuses = [
    "Pending",
    "Processing",
    "Shipped",
    "Delivered",
    "Cancelled",
    "Returned",
    "Refunded"
]

def random_datetime(date:date):
    # print (date)
    random_hour= random.randint(0,23)
    random_minute = random.randint(0,59)
    random_second = random.randint(0,59)
    random_datetime= datetime(year=date.year,month=date.month,day=date.day,hour=random_hour,minute=random_minute,second=random_second)
    # print(random_datetime)
    return random_datetime

def generate_orders(req_date):
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

def generate_order_v2(req_date):
    sales_date = date.fromisoformat(req_date) if req_date else date.today()
    if(sales_date>date.today()):
        return jsonify({'error_msg':'date not valid'}),500
    
    # random_datetime= random_datetime(sales_date)

    # orders = Order.query.filter_by(order_timestamp=sales_date).all()
    start = sales_date
    end = sales_date + timedelta(days=1)

    n_order = Order.query.filter(Order.order_timestamp >= start).filter(Order.order_timestamp < end).count()
    # if(orders):
    #     order_list=[i.to_dict() for i in orders]
    if not(n_order):    
        n_order = random.randint(a=50,b=100)
        # order_list = []
        products = Product.query.all()
        customers = Customer.query.all()

        for _ in range(0,n_order):
            n_item = random.randint(a=1,b=4)
            random_order_id=f"ORDER_{uuid4()}"
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

                # random_item['qty']=random.randint(1,3 if random_item['product_price']>50 else 5)
                random_item_qty=random.randint(1,3 if random_item['product_price']>50 else 5)
                # random_item['sub_total']=random_item['qty']*random_item['product_price']
                random_item_sub_total=random_item_qty*random_item['product_price']
                # product_cost+=random_item['sub_total']
                product_cost+=random_item_sub_total
                item_list.append(random_item)
                item_id_set.add(random_item['id'])
                new_order_item = Order_Item(product_id=UUID(random_item['id']),order_id=random_order_id,qty=random_item_qty,sub_total=random_item_sub_total)
                db.session.add(new_order_item)
                # db.session.commit()
                
            shipping_cost = random.randint(10,15 if product_cost>500 else 20) * product_cost/100
            rand_num= random.randint(1,10)
            order_status = 'pending' if rand_num<=5 else 'processing' if rand_num<=7 else 'canceled'
            new_order = Order(order_id=random_order_id,order_status=order_status,customer_id = random_customer.id,shipping_region=random_region,product_cost=product_cost,shipping_cost=shipping_cost,payment_method=random_payment_method,order_timestamp=random_datetime(sales_date))
            db.session.add(new_order)
            db.session.commit()

    orders = Order.query.filter(Order.order_timestamp >= start).filter(Order.order_timestamp < end).all()
    order_list=[i.to_dict() for i in orders]
    return order_list,sales_date
       
## pending -> processed -> shipped -> delivered
def get_new_order_status(status:str): 
    rand_num = random.randint(1,100)
    match status.lower():
        case "pending":
            new_status = "processing" if rand_num < 80 else "canceled"
        case 'processing':
            new_status = "shipped" if rand_num < 95 else "refunded"
        case 'shipped':
            new_status = "delivered" if rand_num < 97 else "failed shipping, refunded"
    return new_status

def update_order_status():
    pending_orders = Order.query.filter(Order.order_status.like('pending')).filter(Order.order_timestamp<date.today()).all()
    for i in pending_orders:
        i.order_status = get_new_order_status('pending')

    processed_orders = Order.query.filter(Order.order_status=='processing').filter(Order.order_timestamp<date.today()-timedelta(days=1)).all()
    for i in processed_orders:
        i.order_status = get_new_order_status('processing')

    shipped_orders = Order.query.filter(Order.order_status=='shipped').filter(Order.order_timestamp<date.today()-timedelta(days=2)).all()
    for i in shipped_orders:
        if random.randint(1,10)>5:
            i.order_status = get_new_order_status('shipped')

    print(f"pending orders: {len(pending_orders)}")
    print(f"processed orders: {len(processed_orders)}")
    print(f"shipped orders: {len(shipped_orders)}")

    db.session.commit()
    return None