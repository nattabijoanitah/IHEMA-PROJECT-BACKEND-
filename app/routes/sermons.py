from flask import Blueprint, jsonify

from app.models.sermon import Sermon

sermons_bp = Blueprint("sermons", __name__)


@sermons_bp.route("", strict_slashes=False)
@sermons_bp.route("/", strict_slashes=False)
def get_sermons():
    sermons = Sermon.query.order_by(Sermon.created_at.desc()).all()
    return jsonify({"items": [sermon.to_dict() for sermon in sermons]})