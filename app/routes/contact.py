from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.contact import ContactMessage

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/api/contact", methods=["POST"])
def create_contact_message():
    data = request.get_json(silent=True) or {}
    required = ["name", "email", "message"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"message": f"Missing required fields: {', '.join(missing)}"}), 400

    message = ContactMessage(
        name=data.get("name"),
        email=data.get("email"),
        message=data.get("message"),
        status="new",
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({"message": "Message received", "item": message.to_dict()}), 201
