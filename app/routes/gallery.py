from flask import Blueprint, jsonify

from app.models.settings import Media

gallery_bp = Blueprint("gallery", __name__)


@gallery_bp.route("/")
def get_gallery():
    items = Media.query.order_by(Media.id.desc()).all()
    return jsonify({"items": [item.to_dict() for item in items]})