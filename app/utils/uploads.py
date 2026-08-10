import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}


def allowed_image(filename: str) -> bool:
    if not filename:
        return False
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def save_image_upload(file_storage, subfolder: str) -> str:
    if file_storage is None or not getattr(file_storage, "filename", None):
        raise ValueError("No image file was provided")

    if not allowed_image(file_storage.filename):
        raise ValueError("Only image files are allowed")

    filename = secure_filename(file_storage.filename)
    if not filename:
        raise ValueError("Invalid filename")

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "")
    target_dir = os.path.join(upload_folder, subfolder)
    os.makedirs(target_dir, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}_{filename}"
    full_path = os.path.join(target_dir, unique_name)
    file_storage.save(full_path)

    return f"/static/uploads/{subfolder}/{unique_name}"
