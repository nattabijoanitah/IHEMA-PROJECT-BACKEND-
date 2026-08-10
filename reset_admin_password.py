from app import create_app
from app.extensions import db
from app.models.rbac import User


app = create_app()

with app.app_context():
    user = User.query.filter_by(email="admin@ihema.org").first()

    if not user:
        print("Admin user not found")
        raise SystemExit(1)

    user.set_password("password")
    db.session.commit()
    print("Password updated successfully for admin@ihema.org")
