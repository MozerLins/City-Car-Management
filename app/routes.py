from flask import request, jsonify, Blueprint
from app import db
from .models import Owner, Car, User
from flask_jwt_extended import create_access_token, jwt_required

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(name=name).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "Invalid username or password!"}), 401

@api.route('/owners', methods=['POST'])
@jwt_required()
def add_owner():
    data = request.get_json()
    new_owner = Owner(name=data['name'])
    db.session.add(new_owner)
    db.session.commit()
    return jsonify({"message": "Owner added successfully."}), 201

@api.route('/owners/<int:owner_id>/cars', methods=['POST'])
@jwt_required()
def add_car(owner_id):
    owner = Owner.query.get_or_404(owner_id)

    if len(owner.cars) >= 3:
        return jsonify({"message": "Owner already has 3 cars."}), 400

    data = request.get_json()
    valid_colors = ['yellow', 'blue', 'gray']
    valid_models = ['hatch', 'sedan', 'convertible']

    if data['color'] not in valid_colors:
        return jsonify({"message": "Invalid car color."}), 400
    if data['model'] not in valid_models:
        return jsonify({"message": "Invalid car model."}), 400

    new_car = Car(color=data['color'], model=data['model'], owner_id=owner_id)
    db.session.add(new_car)
    db.session.commit()
    return jsonify({"message": "Car added successfully."}), 201

@api.route('/owners', methods=['GET'])
@jwt_required()
def get_owners():
    owners = Owner.query.all()
    output = []

    for owner in owners:
        owner_data = {
            "id": owner.id,
            "name": owner.name,
            "opportunity": owner.opportunity,
            "cars": []
        }
        for car in owner.cars:
            owner_data["cars"].append({
                "id": car.id,
                "color": car.color,
                "model": car.model
            })
        output.append(owner_data)

    return jsonify(output), 200

@api.route('/owners/<int:owner_id>', methods=['GET'])
@jwt_required()
def get_owner(owner_id):
    owner = Owner.query.get_or_404(owner_id)
    owner_data = {
        "id": owner.id,
        "name": owner.name,
        "opportunity": owner.opportunity,
        "cars": []
    }
    for car in owner.cars:
        owner_data["cars"].append({
            "id": car.id,
            "color": car.color,
            "model": car.model
        })
    return jsonify(owner_data), 200

@api.route('/cars/<int:car_id>', methods=['GET'])
@jwt_required()
def get_car(car_id):
    car = Car.query.get_or_404(car_id)
    car_data = {
        "id": car.id,
        "color": car.color,
        "model": car.model,
        "owner_id": car.owner_id
    }
    return jsonify(car_data), 200
