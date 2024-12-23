from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Customer
from app import db, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
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
    
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200