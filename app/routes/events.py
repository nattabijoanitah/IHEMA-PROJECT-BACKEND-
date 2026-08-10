from flask import Blueprint, jsonify

from app.models.event import Event

events_bp = Blueprint("events", __name__)


@events_bp.route("/")
def get_events():
    events = Event.query.order_by(Event.created_at.desc()).all()
    return jsonify({"items": [event.to_dict() for event in events]})