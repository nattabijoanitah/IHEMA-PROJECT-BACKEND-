from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models.prayer import PrayerRequest

prayer_bp = Blueprint("prayer", __name__)


@prayer_bp.route("/api/prayer-requests", methods=["POST"])
def create_prayer_request():
    data = request.get_json(silent=True) or {}
    required = ["name", "message"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify({"message": f"Missing required fields: {', '.join(missing)}"}), 400

    prayer_request = PrayerRequest(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        message=data.get("message"),
        status="new",
    )
    db.session.add(prayer_request)
    db.session.commit()
    return jsonify({"message": "Prayer request submitted", "item": prayer_request.to_dict()}), 201
