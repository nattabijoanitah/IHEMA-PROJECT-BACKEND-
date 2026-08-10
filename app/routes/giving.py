from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.giving import Giving

giving_bp = Blueprint("giving", __name__)


@giving_bp.route("/giving", methods=["POST"])
def create_giving():
    data = request.get_json(silent=True) or {}

    donor_name = data.get("donor_name")
    email = data.get("email")
    amount = data.get("amount")

    if not donor_name or not email or not amount:
        return jsonify({"message": "donor_name, email, and amount are required"}), 400

    record = Giving(
        donor_name=donor_name,
        email=email,
        amount=amount,
        currency=data.get("currency", "UGX"),
        purpose=data.get("purpose", "Tithe"),
        payment_method=data.get("payment_method"),
        status="pending",
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Giving record created", "item": record.to_dict()}), 201