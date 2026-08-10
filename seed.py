from app import create_app
from app.extensions import db
from app.models.rbac import Role, Permission, User


app = create_app()


with app.app_context():

    # Create permissions
    permissions = [
        ("manage_pages", "Create and edit website pages"),
        ("manage_navigation", "Manage website menus"),
        ("manage_users", "Manage admin users"),
        ("manage_settings", "Manage website settings"),
        ("manage_content", "Manage website content"),
        ("manage_sermons", "Manage sermons"),
        ("manage_events", "Manage events"),
        ("manage_gallery", "Manage gallery"),
    ]


    for code, description in permissions:

        existing = Permission.query.filter_by(code=code).first()

        if not existing:

            permission = Permission(
                code=code,
                description=description
            )

            db.session.add(permission)



    # Create roles
    roles = [
        ("super_admin", "Full system access"),
        ("admin", "Manage website content and users"),
        ("editor", "Edit website content"),
        ("client", "Read-only access"),
    ]


    for name, description in roles:

        existing = Role.query.filter_by(name=name).first()

        if not existing:

            role = Role(
                name=name,
                description=description
            )

            db.session.add(role)


    db.session.commit()


    # Give all permissions to super_admin

    super_admin = Role.query.filter_by(
        name="super_admin"
    ).first()


    all_permissions = Permission.query.all()

    super_admin.permissions = all_permissions


    db.session.commit()


    # Create first super admin user

    existing_user = User.query.filter_by(
        email="admin@ihema.org"
    ).first()


    if not existing_user:

        admin = User(
            full_name="IHEMA Super Admin",
            email="admin@ihema.org",
            role=super_admin
        )

        admin.set_password("Admin@12345")

        db.session.add(admin)

        db.session.commit()

        print("Super admin created successfully!")

    else:

        print("Admin already exists!")


    print("Roles and permissions seeded successfully!")