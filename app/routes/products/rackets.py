from flask import Blueprint, jsonify, request
from models import Racket, Brand, db

rackets_bp = Blueprint('rackets', __name__)

@rackets_bp.route('/', methods=['GET', 'POST'])
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


@rackets_bp.route('/<string:id>', methods=['GET'])
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
