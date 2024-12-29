from flask import Blueprint, jsonify, request
from models import Shoes,Brand, db

shoes_bp = Blueprint('shoes', __name__)

@shoes_bp.route('/', methods=['GET', 'POST'])
def handle_shoes():
    if request.method == 'POST':
        data = request.get_json()
        new_shoes = Shoes(
            product_id=data['product_id'],
            product_name=data['product_name'],
            brand=Brand[data['brand']],
            price=data['price'],
            description=data['description'],
            status=data['status'],
            sales=data['sales'],
            stock=data['stock'],
            available_location=data['available_location'],
            color=data['color'],
            size=data['size'],
            available_size=data['available_size'],
            technology=data['technology']
        )
        db.session.add(new_shoes)
        db.session.commit()
        return jsonify({'message': 'Shoes created successfully'}), 201

    elif request.method == 'GET':
        shoes = Shoes.query.all()
        shoes_data = [
            {
                'product_id': shoe.product_id,
                'product_name': shoe.product_name,
                'brand': shoe.brand,
                'price': shoe.price,
                'description': shoe.description,
                'status': shoe.status,
                'sales': shoe.sales,
                'stock': shoe.stock,
                'available_location': shoe.available_location,
                'color': shoe.color,
                'size': shoe.size,
                'available_size': shoe.available_size,
                'technology': shoe.technology
            }
            for shoe in shoes
        ]
        return jsonify(shoes_data), 200
