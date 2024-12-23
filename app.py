from datetime import timedelta

from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies)
from flask_migrate import Migrate
from werkzeug.security import check_password_hash

from models import Brand, Racket, Shoes, Shuttlecock, User, Customer, Admin, db

app = Flask(__name__)

CORS(app, supports_credentials=True)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:BenCuber%402601@localhost/badminton'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'BenCuber@2002'
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
# Create the database tables
with app.app_context():
    db.create_all()

# Models (same as before, assuming they are defined here)

# 2. Routes for User Model
@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        data = request.get_json()
        new_user = User(
            username=data['username'],
            mail=data['mail'],
            phone_number=data['phone_number'],
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

    elif request.method == 'GET':
        users = User.query.all()
        users_data = [
            {
                'user_id': str(user.user_id),  # Convert UUID to string if needed
                'username': user.username,
                'mail': user.mail,
                'phone_number': user.phone_number
            }
            for user in users
        ]
        return jsonify(users_data), 200

@app.route('/register/<string:role>', methods=['POST'])
def register_user(role):
    data = request.get_json()

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    if role.lower() == 'customer':
        # Create a new Customer
        new_user = Customer(
            username=data['username'],
            mail=data['mail'],
            phone_number=data['phone_number'],
            password=hashed_password,
            address=data['address']  # Customer-specific field
        )
    elif role.lower() == 'admin':
        # Create a new Admin
        new_user = Admin(
            username=data['username'],
            mail=data['mail'],
            phone_number=data['phone_number'],
            password=hashed_password,
            branch_id=data['branch_id']  # Admin-specific field
        )
    else:
        return jsonify({'error': 'Invalid role. Choose either "customer" or "admin".'}), 400

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': f'{role.capitalize()} registered successfully.'}), 201


@app.route('/users/<uuid:userid>', methods=['GET'])
@jwt_required()  # Protect this route
def get_user_by_id(userid):
    # Verify if the current user is the one making the request
    current_user = get_jwt_identity()

    # Query the user by UserID
    user = User.query.filter_by(UserID=userid).first()

    if user:
        # Ensure that the user making the request is the same as the one being queried
        if user.UserID != current_user:
            return jsonify({'message': 'Unauthorized access'}), 403

        return jsonify({
            'UserID': str(user.UserID),  # Convert UUID to string if needed
            'Username': user.Username,
            'mail': user.mail,
            'Phonenumber': user.Phonenumber
        }), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/users/<string:username>', methods=['GET'])
@jwt_required()  # Protect this route
def get_user_by_name(username):
    # Verify if the current user is the one making the request
    current_user = get_jwt_identity()

    # Query the user by Username
    user = User.query.filter_by(Username=username).first()

    if user:
        # Ensure that the user making the request is the same as the one being queried
        if user.Username != current_user:
            return jsonify({'message': 'Unauthorized access'}), 403

        return jsonify({
            'UserID': str(user.UserID),  # Convert UUID to string if needed
            'Username': user.Username,
            'mail': user.mail,
            'Phonenumber': user.Phonenumber
        }), 200
    else:
        return jsonify({'message': 'User not found'}), 404

# 3. Routes for Product Models (Racket, Shoes, Shuttlecock)

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(mail=data['mail']).first()

#     if user and check_password_hash(user.password, data['password']):
#         # Create an access token
#         access_token = create_access_token(identity=user.mail, expires_delta=timedelta(days=1))

#         # Set the access token as a cookie
#         resp = jsonify({'login': True})
#         set_access_cookies(resp, access_token)

#         return resp, 200
#     else:
#         return jsonify({'login': False}), 401
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print('Received data:', data)
        
        email = data.get('email')
        password = data.get('password')
        print('Extracted email:', email)
        print('Extracted password:', password)

        # Validate credentials logic...
        if not email or not password:
            return jsonify({"message": "Missing email or password"}), 400
        
        # Check user existence and validate password...
        user = Customer.query.filter_by(mail=email).first()
        print('User found:', user, user.password, password)
        if user and bcrypt.check_password_hash(user.password, password):  # Using bcrypt to check password
            return jsonify({
                "user_id": str(user.user_id),
                "username": user.username,
                "mail": user.mail,
                "phone_number": user.phone_number
            })
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print('Error:', e)
        return jsonify({"message": "An error occurred"}), 500

@app.route('/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200



@app.route('/rackets', methods=['GET', 'POST'])
def handle_rackets():
    if request.method == 'POST':
        data = request.get_json()
        new_racket = Racket(
            product_id=data['product_id'],
            product_name=data['product_name'],
            image_url=data['image_url'],
            brand=Brand[data['brand']],
            price=data['price'],
            description=data['description'],
            status=data['status'],
            sales=data['sales'],
            stock=data['stock'],
            available_location=data['available_location'],
            line=data['line'],
            stiffness=data['stiffness'],
            weight=data['weight'],
            balance=data['balance'],
            max_tension=data['max_tension'],
            length=data['length'],
            technology=data['technology']
        )
        db.session.add(new_racket)
        db.session.commit()
        return jsonify({'message': 'Racket created successfully'}), 201

    elif request.method == 'GET':
        rackets = Racket.query.all()
        rackets_data = [
            {
                'product_id': racket.product_id,
                'product_name': racket.product_name,
                'image_url': racket.image_url,
                'brand': racket.brand.value,
                'price': str(racket.price),
                'description': racket.description,
                'status': racket.status,
                'sales': racket.sales,
                'stock': racket.stock,
                'available_location': racket.available_location,
                'line': racket.line,
                'stiffness': racket.stiffness,
                'weight': racket.weight,
                'balance': racket.balance,
                'max_tension': racket.max_tension,
                'length': str(racket.length),
                'technology': racket.technology
            }
            for racket in rackets
        ]
        return jsonify(rackets_data), 200

@app.route('/rackets/<string:id>', methods=["GET"])
def get_racket_by_id(id):
    # Query the racket by product_id
    racket = Racket.query.filter_by(product_id=id).first()
    
    if racket:
        racket_data = {
            'product_id': racket.product_id,
            'product_name': racket.product_name,
            'image_url': racket.image_url,
            'brand': racket.brand.value,
            'price': str(racket.price),
            'description': racket.description,
            'status': racket.status,
            'sales': racket.sales,
            'stock': racket.stock,
            'available_location': racket.available_location,
            'line': racket.line,
            'stiffness': racket.stiffness,
            'weight': racket.weight,
            'balance': racket.balance,
            'max_tension': racket.max_tension,
            'length': str(racket.length),
            'technology': racket.technology
        }
        return jsonify(racket_data), 200
    else:
        return jsonify({'error': 'Racket not found'}), 404




@app.route('/shoes', methods=['GET', 'POST'])
def handle_shoes():
    if request.method == 'POST':
        data = request.get_json()
        new_shoes = Shoes(
            ProductID=data['product_id'],
            ProductName=data['product_name'],
            Brand=data['brand'],
            Price=data['price'],
            Description=data['description'],
            Status=data['status'],
            Sales=data['sales'],
            Stock=data['stock'],
            AvailableLocation=data['available_location'],
            Color=data['color'],
            Size=data['size'],
            AvailableSize=data['available_size'],
            Technology=data['technology']
        )
        db.session.add(new_shoes)
        db.session.commit()
        return jsonify({'message': 'Shoes created successfully'}), 201

    elif request.method == 'GET':
        shoes = Shoes.query.all()
        shoes_data = [
            {
                'ProductID': shoe.ProductID,
                'ProductName': shoe.ProductName,
                'Brand': shoe.Brand,
                'Price': str(shoe.Price),
                'Description': shoe.Description,
                'Status': shoe.Status,
                'Sales': shoe.Sales,
                'Stock': shoe.Stock,
                'AvailableLocation': shoe.AvailableLocation,
                'Color': shoe.Color,
                'Size': shoe.Size,
                'AvailableSize': shoe.AvailableSize,
                'Technology': shoe.Technology
            }
            for shoe in shoes
        ]
        return jsonify(shoes_data), 200


@app.route('/shuttlecocks', methods=['GET', 'POST'])
def handle_shuttlecocks():
    if request.method == 'POST':
        data = request.get_json()
        new_shuttlecock = Shuttlecock(
            ProductID=data['product_id'],
            ProductName=data['product_name'],
            Brand=data['brand'],
            Price=data['price'],
            Description=data['description'],
            Status=data['status'],
            Sales=data['sales'],
            Stock=data['stock'],
            AvailableLocation=data['available_location'],
            ShuttleType=data['shuttle_type'],
            Speed=data['speed'],
            NoPerTube=data['no_per_tube']
        )
        db.session.add(new_shuttlecock)
        db.session.commit()
        return jsonify({'message': 'Shuttlecock created successfully'}), 201

    elif request.method == 'GET':
        shuttlecocks = Shuttlecock.query.all()
        shuttlecocks_data = [
            {
                'ProductID': shuttlecock.ProductID,
                'ProductName': shuttlecock.ProductName,
                'Brand': shuttlecock.Brand,
                'Price': str(shuttlecock.Price),
                'Description': shuttlecock.Description,
                'Status': shuttlecock.Status,
                'Sales': shuttlecock.Sales,
                'Stock': shuttlecock.Stock,
                'AvailableLocation': shuttlecock.AvailableLocation,
                'ShuttleType': shuttlecock.ShuttleType,
                'Speed': shuttlecock.Speed,
                'NoPerTube': shuttlecock.NoPerTube
            }
            for shuttlecock in shuttlecocks
        ]
        return jsonify(shuttlecocks_data), 200


if __name__ == '__main__':
    app.run(debug=True)