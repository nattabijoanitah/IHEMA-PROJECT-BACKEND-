from app import create_app
from app.models.rbac import User


email = "admin@ihema.org"
password = "password"


app = create_app()

with app.app_context():
    user = User.query.filter_by(email=email).first()

    print(f"User exists: {user is not None}")
    if user is None:
        print("User id: None")
        print("User email: None")
        print("User role: None")
        print("Stored password_hash: None")
        print("Password check result: False")
    else:
        print(f"User id: {user.id}")
        print(f"User email: {user.email}")
        print(f"User role: {user.role.name if user.role else None}")
        print(f"Stored password_hash: {user.password_hash}")
        print(f"Password check result: {user.check_password(password)}")
