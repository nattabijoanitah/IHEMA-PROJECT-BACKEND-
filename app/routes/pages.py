from flask import Blueprint, jsonify

from app.models.page import Page

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def get_pages():
    pages = Page.query.order_by(Page.id.asc()).all()
    return jsonify({"items": [page.to_dict() for page in pages]})