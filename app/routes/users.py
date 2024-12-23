from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from app import db, bcrypt
from models import User, Customer, Admin

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
def get_users():
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

@users_bp.route('/<uuid:userid>', methods=['GET'])
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

@users_bp.route('', methods=['POST'])
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
