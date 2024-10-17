from datetime import timedelta

from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required,
                                set_access_cookies)
from flask_migrate import Migrate

from models import Brand, Racket, Shoes, Shuttlecock, User, db

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
@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'POST':
        # Parse request data
        data = request.get_json()
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        # Create a new user with hashed password
        new_user = User(
            Username=data['username'],
            mail=data['mail'],
            Phonenumber=data['phonenumber'],
            password=hashed_password  # Store the hashed password
        )

        # Add to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201

    elif request.method == 'GET':
        # Fetch all users (excluding the password)
        users = User.query.all()
        users_data = [
            {
                'UserID': user.UserID,
                'Username': user.Username,
                'mail': user.mail,
                'Phonenumber': user.Phonenumber,
            }
            for user in users
        ]

        return jsonify(users_data), 200
#     # 4. Route for getting a single user by UUID
# @app.route('/users/<uuid:user_id>', methods=['GET'])
# def get_user(user_id):
#     # Query the user by UUID
#     user = User.query.filter_by(UserID=user_id).first()

#     if user:
#         return jsonify({
#             'UserID': user.UserID,
#             'Username': user.Username,
#             'mail': user.mail,
#             'Phonenumber': user.Phonenumber
#         }), 200
#     else:
#         return jsonify({'message': 'User not found'}), 404
    
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

@app.route('/rackets', methods=['GET', 'POST'])
def handle_rackets():
    if request.method == 'POST':
        data = request.get_json()
        new_racket = Racket(
            ProductID=data['product_id'],
            ProductName=data['product_name'],
            ImageUrl=data['image_url'],
            Brand=Brand[data['brand']],
            Price=data['price'],
            Description=data['description'],
            Status=data['status'],
            Sales=data['sales'],
            Stock=data['stock'],
            AvailableLocation=data['available_location'],
            Line=data['line'],
            Stiffness=data['stiffness'],
            Weight=data['weight'],
            Balance=data['balance'],
            MaxTension=data['max_tension'],
            Length=data['length'],
            Technology=data['technology']
        )
        db.session.add(new_racket)
        db.session.commit()
        return jsonify({'message': 'Racket created successfully'}), 201

    elif request.method == 'GET':
        # Fetch all rackets
        rackets = Racket.query.all()
        rackets_data = [
            {
                'ProductID': racket.ProductID,
                'ProductName': racket.ProductName,
                'ImageUrl': racket.ImageUrl,
                'Brand': racket.Brand.value,
                'Price': str(racket.Price),  # Convert decimal to string for JSON compatibility
                'Description': racket.Description,
                'Status': racket.Status,
                'Sales': racket.Sales,
                'Stock': racket.Stock,
                'AvailableLocation': racket.AvailableLocation,
                'Line': racket.Line,
                'Stiffness': racket.Stiffness,
                'Weight': racket.Weight,
                'Balance': racket.Balance,
                'MaxTension': racket.MaxTension,
                'Length': str(racket.Length),  # Convert decimal to string for JSON compatibility
                'Technology': racket.Technology
            }
            for racket in rackets
        ]
        return jsonify(rackets_data), 200


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

#4. Authentication
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(Username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Create a JWT token with a 2-hour expiration
    access_token = create_access_token(identity=user.UserID, expires_delta=timedelta(hours=2))

    # Create a response and set the JWT in an HttpOnly cookie
    response = jsonify({'msg': 'Login successful'})
    set_access_cookies(response, access_token)  # Store JWT in HttpOnly cookie
    return response

# A protected route example
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"msg": "You have accessed a protected route"}), 200