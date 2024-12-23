from flask import Blueprint, jsonify, request
from models import Shuttlecock,Brand, db

shuttlecocks_bp = Blueprint('shuttlecock', __name__)

@shuttlecocks_bp.route('/', methods=['GET', 'POST'])
def handle_shuttlecocks():
    if request.method == 'POST':
        data = request.get_json()
        new_shuttlecock = Shuttlecock(
            product_id=data['product_id'],
            product_name=data['product_name'],
            brand=Brand[data['brand']],
            price=data['price'],
            description=data['description'],
            status=data['status'],
            sales=data['sales'],
            stock=data['stock'],
            available_location=data['available_location'],
            shuttle_type=data['shuttle_type'],
            speed=data['speed'],
            no_per_tube=data['no_per_tube']
        )
        db.session.add(new_shuttlecock)
        db.session.commit()
        return jsonify({'message': 'Shuttlecock created successfully'}), 201

    elif request.method == 'GET':
        shuttlecocks = Shuttlecock.query.all()
        shuttlecocks_data = [
            {
                'product_id': shuttlecock.product_id,
                'product_name': shuttlecock.product_name,
                'brand': shuttlecock.brand,
                'price': shuttlecock.price,
                'description': shuttlecock.description,
                'status': shuttlecock.status,
                'sales': shuttlecock.sales,
                'stock': shuttlecock.stock,
                'available_location': shuttlecock.available_location,
                'shuttle_type': shuttlecock.shuttle_type,
                'speed': shuttlecock.speed,
                'no_per_tube': shuttlecock.no_per_tube
            }
            for shuttlecock in shuttlecocks
        ]
        return jsonify(shuttlecocks_data), 200
