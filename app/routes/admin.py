from datetime import datetime

from flask import Blueprint, jsonify, request
from app.models.giving import Giving
from app.extensions import db
from app.models.contact import ContactMessage
from app.models.event import Event
from app.models.page import Page
from app.models.prayer import PrayerRequest
from app.models.rbac import User
from app.models.sermon import Sermon
from app.models.settings import Media
from app.utils.decorators import admin_required
from app.utils.uploads import save_image_upload

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/giving", methods=["GET"])
@admin_required
def list_giving():
    records = Giving.query.order_by(Giving.created_at.desc()).all()
    return jsonify({"items": [item.to_dict() for item in records]})


@admin_bp.route("/giving/<int:giving_id>", methods=["GET"])
@admin_required
def get_giving(giving_id):
    record = Giving.query.get_or_404(giving_id)
    return jsonify({"item": record.to_dict()})


@admin_bp.route("/giving/search", methods=["GET"])
@admin_required
def search_giving():
    email = request.args.get("email")
    if not email:
        return jsonify({"message": "email query param is required"}), 400
    records = Giving.query.filter_by(email=email).order_by(Giving.created_at.desc()).all()
    return jsonify({"items": [item.to_dict() for item in records]})


@admin_bp.route("/giving/<int:giving_id>", methods=["PUT"])
@admin_required
def update_giving_status(giving_id):
    record = Giving.query.get_or_404(giving_id)
    data = request.get_json(silent=True) or {}
    if "status" in data:
        record.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Giving record updated", "item": record.to_dict()})


@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    return jsonify({
        "total_users": User.query.count(),
        "total_sermons": Sermon.query.count(),
        "total_events": Event.query.count(),
        "total_gallery_items": Media.query.count(),
        "total_prayer_requests": PrayerRequest.query.count(),
        "total_messages": ContactMessage.query.count(),
    })


@admin_bp.route("/sermons", methods=["POST"])
@admin_required
def create_sermon():
    data = request.form.to_dict(flat=True)
    title = data.get("title")
    if not title:
        return jsonify({"message": "title is required"}), 400

    image_url = data.get("image_url")
    if "image_file" in request.files and request.files["image_file"].filename:
        try:
            image_url = save_image_upload(request.files["image_file"], "sermons")
        except ValueError as exc:
            return jsonify({"message": str(exc)}), 400

    sermon = Sermon(
        title=title,
        description=data.get("description"),
        scripture_reference=data.get("scripture_reference"),
        image_url=image_url,
    )
    db.session.add(sermon)
    db.session.commit()
    return jsonify({"message": "Sermon created", "item": sermon.to_dict()}), 201


@admin_bp.route("/sermons", methods=["GET"])
@admin_required
def list_sermons():
    sermons = Sermon.query.order_by(Sermon.created_at.desc()).all()
    return jsonify({"items": [item.to_dict() for item in sermons]})


@admin_bp.route("/sermons/<int:sermon_id>", methods=["PUT"])
@admin_required
def update_sermon(sermon_id):
    sermon = Sermon.query.get_or_404(sermon_id)
    data = request.form.to_dict(flat=True)
    if "image_file" in request.files and request.files["image_file"].filename:
        try:
            sermon.image_url = save_image_upload(request.files["image_file"], "sermons")
        except ValueError as exc:
            return jsonify({"message": str(exc)}), 400
    for field in ["title", "description", "scripture_reference", "image_url"]:
        if field in data and data[field] not in {None, ""}:
            setattr(sermon, field, data[field])
    db.session.commit()
    return jsonify({"message": "Sermon updated", "item": sermon.to_dict()})


@admin_bp.route("/sermons/<int:sermon_id>", methods=["DELETE"])
@admin_required
def delete_sermon(sermon_id):
    sermon = Sermon.query.get_or_404(sermon_id)
    db.session.delete(sermon)
    db.session.commit()
    return jsonify({"message": "Sermon deleted"})


@admin_bp.route("/events", methods=["POST"])
@admin_required
def create_event():
    data = request.form.to_dict(flat=True)
    title = data.get("title")
    if not title:
        return jsonify({"message": "title is required"}), 400

    image_url = data.get("image_url")
    if "image_file" in request.files and request.files["image_file"].filename:
        try:
            image_url = save_image_upload(request.files["image_file"], "events")
        except ValueError as exc:
            return jsonify({"message": str(exc)}), 400

    event_date = None
    if data.get("event_date"):
        try:
            event_date = datetime.fromisoformat(data["event_date"])
        except ValueError:
            event_date = None

    event = Event(
        title=title,
        description=data.get("description"),
        location=data.get("location"),
        event_date=event_date,
        image_url=image_url,
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({"message": "Event created", "item": event.to_dict()}), 201


@admin_bp.route("/events", methods=["GET"])
@admin_required
def list_events():
    events = Event.query.order_by(Event.created_at.desc()).all()
    return jsonify({"items": [item.to_dict() for item in events]})


@admin_bp.route("/events/<int:event_id>", methods=["PUT"])
@admin_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.form.to_dict(flat=True)
    if "image_file" in request.files and request.files["image_file"].filename:
        try:
            event.image_url = save_image_upload(request.files["image_file"], "events")
        except ValueError as exc:
            return jsonify({"message": str(exc)}), 400
    for field in ["title", "description", "location", "image_url"]:
        if field in data and data[field] not in {None, ""}:
            setattr(event, field, data[field])
    if "event_date" in data and data["event_date"] not in {None, ""}:
        try:
            event.event_date = datetime.fromisoformat(data["event_date"])
        except ValueError:
            return jsonify({"message": "event_date must be an ISO-8601 datetime"}), 400
    db.session.commit()
    return jsonify({"message": "Event updated", "item": event.to_dict()})


@admin_bp.route("/events/<int:event_id>", methods=["DELETE"])
@admin_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"})


@admin_bp.route("/gallery", methods=["POST"])
@admin_required
def create_gallery_item():
    if "file" not in request.files:
        return jsonify({"message": "An image file is required"}), 400

    file_storage = request.files["file"]

    try:
        relative_path = save_image_upload(file_storage, "gallery")
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400

    media = Media(filename=file_storage.filename, url=relative_path, media_type="image")
    db.session.add(media)
    db.session.commit()

    return jsonify({"message": "Gallery image uploaded", "item": media.to_dict()}), 201


@admin_bp.route("/gallery", methods=["GET"])
@admin_required
def list_gallery_items():
    items = Media.query.order_by(Media.id.desc()).all()
    return jsonify({"items": [item.to_dict() for item in items]})

@admin_bp.route("/gallery/<int:item_id>", methods=["PUT"])
@admin_required
def update_gallery_item(item_id):
    media = Media.query.get_or_404(item_id)
    data = request.form.to_dict(flat=True)

    if "file" in request.files and request.files["file"].filename:
        try:
            media.url = save_image_upload(request.files["file"], "gallery")
        except ValueError as exc:
            return jsonify({"message": str(exc)}), 400
        media.filename = request.files["file"].filename

    if "filename" in data and data["filename"]:
        media.filename = data["filename"]

    db.session.commit()
    return jsonify({"message": "Gallery item updated", "item": media.to_dict()})


@admin_bp.route("/gallery/<int:item_id>", methods=["DELETE"])
@admin_required
def delete_gallery_item(item_id):
    media = Media.query.get_or_404(item_id)
    db.session.delete(media)
    db.session.commit()
    return jsonify({"message": "Gallery item deleted"})


@admin_bp.route("/pages", methods=["POST"])
@admin_required
def create_page():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    slug = data.get("slug")
    if not title or not slug:
        return jsonify({"message": "title and slug are required"}), 400
    page = Page(title=title, slug=slug, meta_title=data.get("meta_title"), meta_description=data.get("meta_description"), is_published=data.get("is_published", False), is_homepage=data.get("is_homepage", False))
    db.session.add(page)
    db.session.commit()
    return jsonify({"message": "Page created", "page": page.to_dict()}), 201


@admin_bp.route("/pages/<int:page_id>", methods=["PUT"])
@admin_required
def update_page(page_id):
    page = Page.query.get_or_404(page_id)
    data = request.get_json(silent=True) or {}
    for field in ["title", "slug", "meta_title", "meta_description", "is_published", "is_homepage"]:
        if field in data:
            setattr(page, field, data[field])
    db.session.commit()
    return jsonify({"message": "Page updated", "page": page.to_dict()})


@admin_bp.route("/pages/<int:page_id>", methods=["DELETE"])
@admin_required
def delete_page(page_id):
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    return jsonify({"message": "Page deleted"})


@admin_bp.route("/prayer-requests", methods=["GET"])
@admin_required
def list_prayer_requests():
    requests = PrayerRequest.query.order_by(PrayerRequest.created_at.desc()).all()
    return jsonify({"items": [item.to_dict() for item in requests]})


@admin_bp.route("/prayer-requests/<int:request_id>", methods=["PUT"])
@admin_required
def update_prayer_request(request_id):
    prayer_request = PrayerRequest.query.get_or_404(request_id)
    data = request.get_json(silent=True) or {}
    if "status" in data:
        prayer_request.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Prayer request updated", "item": prayer_request.to_dict()})


@admin_bp.route("/prayer-requests/<int:request_id>", methods=["DELETE"])
@admin_required
def delete_prayer_request(request_id):
    prayer_request = PrayerRequest.query.get_or_404(request_id)
    db.session.delete(prayer_request)
    db.session.commit()
    return jsonify({"message": "Prayer request deleted"})


@admin_bp.route("/messages", methods=["GET"])
@admin_required
def list_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify({"items": [item.to_dict() for item in messages]})


@admin_bp.route("/messages/<int:message_id>", methods=["DELETE"])
@admin_required
def delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"})
