
from app import create_app
from app.extensions import db
from app.models.rbac import User, Role

app = create_app()

with app.app_context():
    role = Role.query.filter_by(name="admin").first()

    if not role:
        print("ERROR: admin role not found.")
    else:
        existing_user = User.query.filter_by(
            email="admin@ihema.org"
        ).first()

        if existing_user:
            print("Admin user already exists.")
        else:
            user = User(
                full_name="IHEMA Administrator",
                email="admin@ihema.org",
                role_id=role.id,
                is_active=True
            )

            user.set_password("IhemaAdmin123!")

            db.session.add(user)
            db.session.commit()

            print("ADMIN USER CREATED SUCCESSFULLY")
            print("Email: admin@ihema.org")
            print("Password: IhemaAdmin123!")
            print("Role:", role.name)
