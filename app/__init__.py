from flask import Flask, app

from .extensions import db, migrate, jwt, cors, bcrypt
from config import Config

from .routes.users import users_bp


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


    # Import models
    from app.models.rbac import (
        User,
        Role,
        Permission,
        role_permissions
    )

    from app.models.giving import Giving
    from app.models.page import Page
    from app.models.prayer import PrayerRequest
    from app.models.contact import ContactMessage
    from app.models.sermon import Sermon
    from app.models.event import Event
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


    # Import blueprints
    from app.routes.auth import auth_bp
    from app.routes.pages import pages_bp
    from app.routes.sermons import sermons_bp
    from app.routes.events import events_bp
    from app.routes.gallery import gallery_bp
    from app.routes.admin import admin_bp
    from app.routes.prayer import prayer_bp
    from app.routes.contact import contact_bp
    from app.routes.giving import giving_bp


    # Register blueprints
    app.register_blueprint(users_bp)

    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        pages_bp,
        url_prefix="/api/pages"
    )

    app.register_blueprint(
        sermons_bp,
        url_prefix="/api/sermons"
    )

    app.register_blueprint(
        events_bp,
        url_prefix="/api/events"
    )

    app.register_blueprint(
        gallery_bp,
        url_prefix="/api/gallery"
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/api/admin"
    )

    app.register_blueprint(prayer_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(giving_bp, url_prefix="/api")

    # Test route
    @app.route("/")
    def home():
        return {
            "message": "Ihema API is running successfully"
        }

    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200


    return app