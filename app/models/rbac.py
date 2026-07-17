from datetime import datetime

from app.extensions import db, bcrypt


# Association table: which permissions a role carries

role_permissions = db.Table(

    "role_permissions",

    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id"),
        primary_key=True
    ),

    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permissions.id"),
        primary_key=True
    ),

)



class Role(db.Model):

    """
    e.g. super_admin, admin, editor, client

    super_admin -> full system access, manages other admins
    admin       -> manages content, pages, users
    editor      -> can edit content sections
    client      -> read-only access
    """

    __tablename__ = "roles"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )


    description = db.Column(
        db.String(255)
    )


    users = db.relationship(
        "User",
        back_populates="role",
        lazy="dynamic"
    )


    permissions = db.relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="joined"
    )



    def has_permission(self, code: str) -> bool:

        return any(
            p.code == code
            for p in self.permissions
        )



    def to_dict(self, with_permissions=False):

        data = {

            "id": self.id,

            "name": self.name,

            "description": self.description

        }


        if with_permissions:

            data["permissions"] = [
                p.code
                for p in self.permissions
            ]


        return data





class Permission(db.Model):

    """
    Permission codes:
    manage_pages,
    manage_navigation,
    manage_users,
    manage_settings
    """

    __tablename__ = "permissions"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    code = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )


    description = db.Column(
        db.String(255)
    )



    roles = db.relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )



    def to_dict(self):

        return {

            "id": self.id,

            "code": self.code,

            "description": self.description

        }





class User(db.Model):

    __tablename__ = "users"



    id = db.Column(
        db.Integer,
        primary_key=True
    )


    full_name = db.Column(
        db.String(120),
        nullable=False
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )


    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False
    )


    role = db.relationship(
        "Role",
        back_populates="users"
    )


    is_active = db.Column(
        db.Boolean,
        default=True
    )


    avatar_url = db.Column(
        db.String(255)
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



    def set_password(self, raw_password: str):

        self.password_hash = (
            bcrypt
            .generate_password_hash(raw_password)
            .decode("utf-8")
        )



    def check_password(self, raw_password: str) -> bool:

        return bcrypt.check_password_hash(
            self.password_hash,
            raw_password
        )



    def has_permission(self, code: str) -> bool:

        return (
            self.role.has_permission(code)
            if self.role
            else False
        )



    def to_dict(self):

        return {

            "id": self.id,

            "full_name": self.full_name,

            "email": self.email,

            "role": (
                self.role.name
                if self.role
                else None
            ),

            "is_active": self.is_active,

            "avatar_url": self.avatar_url,

            "created_at":
            (
                self.created_at.isoformat()
                if self.created_at
                else None
            )

        }