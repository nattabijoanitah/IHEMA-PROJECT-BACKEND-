from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from app.extensions import db
from app.models.rbac import User, Role

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role_name = data.get("role", "admin")

    if not full_name or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400

    existing = User.query.filter_by(email=email).first()

    if existing:
        return jsonify({"message": "Email already exists"}), 409

    role = Role.query.filter_by(name=role_name).first()

    if not role:
        return jsonify({"message": "Role not found"}), 404

    user = User(
        full_name=full_name,
        email=email,
        role=role
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "user": user.to_dict()
    })


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user.to_dict())