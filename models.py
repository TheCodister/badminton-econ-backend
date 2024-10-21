import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, UUID

db = SQLAlchemy()

# Brand Enum
from enum import Enum as PyEnum

class Brand(PyEnum):
    LINING = 'Lining'
    YONEX = 'Yonex'
    VICTOR = 'Victor'
    MIZUNO = 'Mizuno'
    VS = 'VS'
    KUMPOO = 'Kumpoo'
    APACS = 'Apacs'
    PROACE = 'Proace'
    FLEET = 'Fleet'
    FLYPOWER = 'Flypower'
    RESON = 'Reson'

# User Model
class User(db.Model):
    __tablename__ = 'users'
    __abstract__ = True  # This makes it an abstract base class

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Customer(User):
    __tablename__ = 'customers'

    address = db.Column(db.Text, nullable=False)
    orders = db.relationship('Order', backref='customer', lazy=True)

class Admin(User):
    __tablename__ = 'admins'

    branch_id = db.Column(db.String(100), nullable=False)
    branch_name = db.Column(db.String(100), nullable=False)

# Product Base Model
class Product(db.Model):
    __tablename__ = 'products'
    __abstract__ = True  # This makes it an abstract base class

    product_id = db.Column(db.String(100), primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.Enum(Brand), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')  # Can be 'available' or 'unavailable'
    sales = db.Column(db.Boolean, default=False)
    stock = db.Column(db.Integer, nullable=False)
    available_location = db.Column(JSON, nullable=False)

# Racket Model
class Racket(Product):
    __tablename__ = 'rackets'
    
    line = db.Column(db.String(100), nullable=False)
    stiffness = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.String(100), nullable=False)
    max_tension = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Numeric(5, 2), nullable=True)
    technology = db.Column(JSON, nullable=True)

# Shoes Model
class Shoes(Product):
    __tablename__ = 'shoes'

    color = db.Column(JSON, nullable=False)
    size = db.Column(JSON, nullable=False)
    available_size = db.Column(JSON, nullable=False)
    technology = db.Column(JSON, nullable=False)

# Shuttlecock Model
class Shuttlecock(Product):
    __tablename__ = 'shuttlecocks'

    shuttle_type = db.Column(db.String(100), nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    no_per_tube = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.user_id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class Branch(db.Model):
    __tablename__ = 'branches'

    branch_id = db.Column(db.String(100), primary_key=True)
    branch_name = db.Column(db.String(100), nullable=False)
    branch_address = db.Column(db.Text, nullable=False)
    branch_phone = db.Column(db.String(15), nullable=False)
    admins = db.relationship('Admin', backref='branch', lazy=True)

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_carts'

    cart_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('customers.user_id'), nullable=False)
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('shopping_carts.cart_id'), nullable=False)
    product_id = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)