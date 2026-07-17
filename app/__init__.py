from flask import Flask

from .extensions import db, migrate, jwt, cors, bcrypt
from config import Config


def create_app():

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    bcrypt.init_app(app)


    # Import models so SQLAlchemy knows them
    from app.models.rbac import (
        User,
        Role,
        Permission,
        role_permissions
    )

    from app.models.page import Page
    from app.models.navigation import MenuItem
    from app.models.hero import HeroSection

    from app.models.content import (
        ContentSection,
        ContentBlock
    )

    from app.models.footer import (
        FooterColumn,
        FooterLink,
        SocialLink
    )

    from app.models.settings import (
        Media,
        SiteSettings
    )


    @app.route("/")
    def home():
        return {
            "message": "Rahmah API is running successfully"
        }


    return app