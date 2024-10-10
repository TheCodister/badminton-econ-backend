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

    UserID = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Username = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(255), unique=True, nullable=False)
    Phonenumber = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Product Base Model
class Product(db.Model):
    __tablename__ = 'products'
    __abstract__ = True  # This makes it an abstract base class

    ProductID = db.Column(db.String(100), primary_key=True)
    ImageUrl = db.Column(db.String(255), nullable=False)
    ProductName = db.Column(db.String(200), nullable=False)
    Brand = db.Column(db.Enum(Brand), nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Status = db.Column(db.String(20), nullable=False, default='available')  # Can be 'available' or 'unavailable'
    Sales = db.Column(db.Boolean, default=False)
    Stock = db.Column(db.Integer, nullable=False)
    AvailableLocation = db.Column(JSON, nullable=False)

# Racket Model
class Racket(Product):
    __tablename__ = 'rackets'
    
    Line = db.Column(db.String(100), nullable=False)
    Stiffness = db.Column(db.String(100), nullable=False)
    Weight = db.Column(db.String(100), nullable=False)
    Balance = db.Column(db.String(100), nullable=False)
    MaxTension = db.Column(db.String(100), nullable=False)
    Length = db.Column(db.Numeric(5, 2), nullable=True)
    Technology = db.Column(JSON, nullable=True)

# Shoes Model
class Shoes(Product):
    __tablename__ = 'shoes'

    Color = db.Column(JSON, nullable=False)
    Size = db.Column(JSON, nullable=False)
    AvailableSize = db.Column(JSON, nullable=False)
    Technology = db.Column(JSON, nullable=False)

# Shuttlecock Model
class Shuttlecock(Product):
    __tablename__ = 'shuttlecocks'

    ShuttleType = db.Column(db.String(100), nullable=False)
    Speed = db.Column(db.Integer, nullable=False)
    NoPerTube = db.Column(db.Integer, nullable=False)
